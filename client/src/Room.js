import { useEffect, useState } from "react";
import { v4 as uuidv4 } from 'uuid';

export default function Room({setAppstate, user, connection, setGamemap}) {

  const [roomstate, setRoomstate] = useState("listroom"); // listroom, indoor
  const [roomlist, setRoomlist] = useState([]);
  const [indoorlist, setIndoorlist] = useState(undefined); // Record status inside a room
	
  const RoomPayloadTemplate = {
    "type": "room",
    "direction": "client2game-server",
    "user-id": user['id'],
    "user-token": user['token']
  }

  connection.onmessage = ((msg) => {
    console.log(msg);
    const payload = JSON.parse(msg.data);
    if (payload['type'] ===  "room" && payload['subtype'] === "list") {
      console.log(payload['rooms']);
      // Check if user is in one room
      const rooms = payload['rooms'];
      let user_in_room = false;
      rooms.forEach((room) => {
        const players = room['players'];
        players.forEach((player) => {
          if (player['id'] === user['id']) {
            user_in_room = true;
            setIndoorlist(room);
          }
        });
      });

      if (user_in_room === false) {
        setRoomlist(payload['rooms']);
        if (roomstate !== "listroom")
          setRoomstate("listroom");
      } else if (user_in_room === true && roomstate != "indoor") {
        setRoomstate("indoor");
      }
    }

    if (payload['type'] === "game" && payload['subtype'] === "map") {
      setGamemap(payload['map']);
      setAppstate("game");
    }
  });

  useEffect(() => {
    let payload = RoomPayloadTemplate;
    payload['subtype'] = "list";
    connection.send(JSON.stringify(payload));
  }, []);

  function ListRoom() {
    const [newRoomName, setNewRoomName] = useState("");

    function handleCreateRoom() {
      let payload = RoomPayloadTemplate;
      payload['subtype'] = "create";
      payload['roomname'] = newRoomName;
      connection.send(JSON.stringify(payload));
    }

    function handleJoinRoom(roomId) {
      let payload = RoomPayloadTemplate;
      payload['subtype'] = "join";
      payload['room-id'] = roomId;
      connection.send(JSON.stringify(payload));
    }

    return (
      <div>
        <div>Rooms</div>
        <br/>
        <input onChange={(e)=>setNewRoomName(e.target.value)}/>
        <button onClick={(e)=>handleCreateRoom()}>Create Room</button>
        <br/>
        {
          roomlist.map((room) => {
            return (
              <div key={uuidv4()}>
                <div>Name: {room.name}</div>
                <div>Owner: {room['owner-id']}</div>
                <div>Player count: {room.players.length}</div>
                <button onClick={(e)=>handleJoinRoom(room.id)}>Join</button>
                <br/>
              </div>
            )
          })
        }
      </div>
    )
  }

  function ListIndoor() {

    function LeaveCloseRoom() {
      function handleClose() {
        let payload = RoomPayloadTemplate;
        payload['subtype'] = "close";
        payload['room-id'] = indoorlist.id;
        connection.send(JSON.stringify(payload));
      }

      function handleLeave() {
        let payload = RoomPayloadTemplate;
        payload['subtype'] = "leave";
        payload['room-id'] = indoorlist.id;
        connection.send(JSON.stringify(payload));
      }

      if (user['id'] === indoorlist['owner-id'])
        return ( <button onClick={(e)=>handleClose()}>Close</button> )
      else
        return ( <button onClick={(e)=>handleLeave()}>Leave</button> )
    }


    function handleReady() {
      let payload = RoomPayloadTemplate;
      payload['subtype'] = "ready";
      payload['room-id'] = indoorlist.id;
      connection.send(JSON.stringify(payload));
    }

    function handleNotReady() {
      let payload = RoomPayloadTemplate;
      payload['subtype'] = "unready";
      payload['room-id'] = indoorlist.id;
      connection.send(JSON.stringify(payload));
    }

    return (
      <div>
        <div>Room: {indoorlist.name}</div><br/>
        <div>Owner: {indoorlist['owner-id']}</div><br/>
        <div>Players:</div><br/>
        {
          indoorlist.players.map((player) => {
            let status = "ready";
            if (player.ready === false)
              status = "not ready";
            return (
              <div key={uuidv4()}>
                <div>ID: {player.id}</div>
                <div>Status: {status}</div>
              </div>
            )
          })
        }
        <button onClick={(e)=>handleReady()}>Ready</button>
        <button onClick={(e)=>handleNotReady()}>Not ready</button>
        <LeaveCloseRoom />
      </div>
    )
  }

  if (roomstate === "listroom") {
    return ( <ListRoom /> );
  } else if (roomstate === "indoor") {
    return ( <ListIndoor /> );
  }
  
  return (
    <div>Hello World!</div>
  );
}