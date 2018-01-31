-module(wihd).
-export([start/1, start/0]).

start() ->
    start(1664).
start(Port) ->
    Pid = spawn_link(fun() ->
			     {ok, Listen} = gen_tcp:listen(Port, [{active, true}]),
			     Linker = spawn(fun () -> linker() end),
			     spawn(fun () -> acceptor(Linker, Listen) end),
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

acceptor(Linker, ListenSocket) ->
    {ok, Socket} = gen_tcp:accept(ListenSocket),
    spawn(fun() ->
		  acceptor(Linker, ListenSocket) end),
    join(Linker, Socket).

join(Linker, Socket) ->
    Linker ! {looking, self()},
    handle(Socket).

handle(Socket) ->
%% Wait to be paired up
    receive
	{connect, Opponent} ->
	    Opponent ! "Connected.",
	    handle(Socket, Opponent);
	_ ->
	    handle(Socket)
    end.


handle(User, Opponent) ->
%% Relay info between User over TCP and Opponent over PM.
    receive
	error ->
	    gen_tcp:close(User);
	{tcp, User, Move} ->
	    Opponent ! {self(), Move},
	    handle(User, Opponent);
	{Opponent, Move} -> 
	    case gen_tcp:send(User, Move) of
		ok -> handle(User, Opponent);
		_ -> Opponent ! error
	     end;
	_ -> handle(User, Opponent)
    end.
