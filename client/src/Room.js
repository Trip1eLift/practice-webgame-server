import { useEffect, useState } from "react";
import { v4 as uuidv4 } from 'uuid';

export default function Room({setAppstate, user, connection}) {

  const [roomstate, setRoomstate] = useState("listroom");
	
  connection.onmessage = ((msg) => {
    console.log(msg);
    const payload = JSON.parse(msg.data);
  });

  useEffect(() => {
    const payload = {
      "type": "room",
      "subtype": "list",
      "direction": "client2game-server",
      "user-id": user['id'],
      "user-token": user['token']
    }
    connection.send(JSON.stringify(payload));
  }, []);
  
  return (
    <div>
      <div>Hello World! ROOM</div>
      
    </div>
  );
}

function room_onrecieve(payload) {
  if (payload['type'] === "room") {

  }
}