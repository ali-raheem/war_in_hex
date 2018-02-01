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
    register_with_linker(Socket).

register_with_linker(Socket) ->
    receive
	{tcp, Socket, Msg} ->
	    Linker = whereis(linker),
	    Linker ! {looking, Msg, self()},
	    wait_for_partnet(Socket)
    end,
    register_with_linker(Socket).

wait_for_partner(Socket) ->
%% Send Linker any game name, wait to be paired by Linker.
    receive
	{connect, Opponent} ->
	    link(Opponent),
	    handle(Socket, Opponent)
    end,
    wait_for_partner(Socket).


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
%% Maintain a proplist of game_names and waiting clients.
%% Add client to wait list or pair with a partner according to game name.
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

