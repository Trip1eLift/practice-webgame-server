import { useEffect, useState } from "react";
import { v4 as uuidv4 } from 'uuid';
import axios from 'axios';

const SERVER_URL = 'ws://127.0.0.1:5001';

export default function Login({setAppstate, setUser, setConnection}) {
	const [id, setId] = useState("");
	const [password, setPassword] = useState("");

	function handleLogin() {
		const path = "http://127.0.0.1:5000/login";
		const body = {
			"id": "jbc5740",
    		"password": "password"
		};
		const headers = {"Content-Type": "application/json"};
		axios.post(path, body, {headers: headers})
			.then((res) => {
				console.log(res.data);
				if (res.data['id'] !== undefined && res.data['token'] !== undefined) {
					

					const Connection = new WebSocket(SERVER_URL);
					
					Connection.onmessage = ((msg) => {
						//console.log(msg.data);
						const payload = JSON.parse(msg.data);
						if (payload['type'] === "login" && payload['subtype'] === "client" && payload['result'] === "allow") {
							setUser(res.data);
							setAppstate("room");
							console.log('WebSocket Client Connected');
						} else {
							Connection.close();
							console.log('WebSocket Client Closed');
						}
					});
					
					Connection.onopen = (() => {
					  	const payload = {
							"type": "login",
							"subtype": "client",
							"direction": "client2game-server",
							"user-id": res.data['id'],
							"user-token": res.data['token']
						}
						Connection.send(JSON.stringify(payload));
					});
					setConnection(Connection);
				}
			})
			.catch((err) => {
				console.error(err);
			});
	}

	return (
		<div>
			<input onChange={(e)=>setId(e.target.value)}/>
			<br/>
			<input onChange={(e)=>setPassword(e.target.value)}/>
			<br/>
			<button onClick={(e)=>handleLogin()}>Login</button>

			<div>{id}</div>
			<div>{password}</div>
		</div>
	)
}