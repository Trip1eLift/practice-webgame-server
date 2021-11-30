import { useState } from "react";
import Login from "./Login";
import Room from "./Room";

export default function App() {

  const [appstate, setAppstate] = useState("login"); // login, room, game
  const [user, setUser] = useState(null);
  const [connection, setConnection] = useState(null);
  const [gamemap, setGamemap] = useState(null);

  if (appstate === "login")
    return ( <Login setAppstate={setAppstate} setUser={setUser} setConnection={setConnection} /> );
  else if (appstate === "room")
    return ( <Room setAppstate={setAppstate} user={user} connection={connection} setGamemap={setGamemap} /> );

  return (
    <div>
      Hello World APP
    </div>
  );
}
