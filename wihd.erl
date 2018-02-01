-module(wihd).
-export([start/1, start/0]).

start() ->
    start(1664).
start(Port) ->
    Pid = spawn_link(fun() ->
			     {ok, Listen} = gen_tcp:listen(Port, [{active, true}]),
			     Linker = spawn(fun () -> linker2() end),
			     register(linker, Linker),
			     spawn(fun () -> acceptor(Listen) end),
			     timer:sleep(infinity)
		     end),
    {ok, Pid}.

linker() ->
    receive
	{looking, Client} ->
	    linker(Client);
	_ ->
	    linker()
    end.
linker(Blue) ->
    receive
	{looking, Red} ->
	    Blue ! {connect, Red},
	    Red ! {connect, Blue},
	    linker();
	 _ ->
	    linker(Blue)
    end.

acceptor(ListenSocket) ->
    {ok, Socket} = gen_tcp:accept(ListenSocket),
    spawn(fun() ->
		  acceptor(ListenSocket) end),
    handle(Socket).


handle(Socket) ->
%% Wait to be paired up
    receive
	{tcp, Socket, Msg} ->
	    Linker = whereis(linker),
	    Linker ! {looking, Msg, self()};
	{connect, Opponent} ->
	    link(Opponent),
	    handle(Socket, Opponent)
    end,
    handle(Socket).


handle(User, Opponent) ->
%% Relay info between User over TCP and Opponent over PM.
    receive
	{tcp, User, Move} ->
	    Opponent ! {self(), Move},
	    handle(User, Opponent);
	{Opponent, Move} -> 
	    case gen_tcp:send(User, Move) of
		ok -> handle(User, Opponent);
		_ -> exit(noproc)
	     end;
	_ -> handle(User, Opponent)
%% Time out after 10 minutes
	after 600000 -> exit(noproc)
    end.

linker2() ->
    linker2([]).
linker2(L) ->
    receive
	{looking, Tag, User} ->
	    case proplists:get_value(Tag, L) of
		undefined ->
		    linker2([{Tag, User}|L]);
		Partner ->
		    User ! {connect, Partner},
		    Partner ! {connect, User},
		    linker2(proplists:delete(tag, L))
	    end
    end,
    linker2(L).

