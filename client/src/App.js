import { useEffect, useState } from "react";
import { v4 as uuidv4 } from 'uuid';

const SERVER_URL = 'ws://127.0.0.1:5001';

let Connection;

export default function App() {

  const [print, setPrint] = useState([]);
  const [rerender, setRerender] = useState(uuidv4()); // This trrigger re-render onmessage
  
  // websocket part
  useEffect(() => {
    Connection = new WebSocket(SERVER_URL);
    Connection.onopen = (() => {
      console.log('WebSocket Client Connected');
    });

    Connection.onmessage = ((msg) => {
      console.log(msg.data);
      let newPrt = print;
      newPrt.push(msg.data);
      setPrint(newPrt);
      setRerender(uuidv4());
    });
  }, []);

  function handleOnclick() {
    const data = {
      type: "message",
      message: "clicked",
      id: uuidv4()
    }
    Connection.send(JSON.stringify(data));
  }

  function Printall() {
    return (<>{print.map((ele) => {
      return <div key={uuidv4()}>{ele}</div>
    })}</>)
  }

  return (
    <div>
      <div>Hello World!</div>
      <button onClick={(e)=>handleOnclick()}>Click me</button>
      <Printall />
      <div></div>
    </div>
  );
}
