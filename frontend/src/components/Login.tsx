import React, { useState } from "react";
import { GenericButton } from "./ButtonUtils";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import  AuthInput  from "./Utils"



export const Login:React.FC = () => {
	const [email, setEmail] = useState<string>("")
	const [password, setPassword] = useState<string>("")
	const [error, setError] = useState<string | null>("")
	const [info, setInfo] = useState<string | null>("")
	const navigate = useNavigate();

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setTimeout(() => {
			setError("");
			setInfo("")
		}, 3000)
		const loginPayload = {
			email,
			password
		}
		try {
			if (!email || !password) {
				setError("Email or password is empty")
				return
			}
			const response = await axios.post("http://localhost:8000/api/auth/login", loginPayload);
			console.log("Login successful: ", response.data)
			setInfo(`Login successful! Welcome ${response.data.username}`)
			setTimeout(() => {
				setEmail("")
				setPassword("")
				navigate("/")
			}, 2000)
		} catch (error: any) {
			console.error("Error: ", error.message)
			setError("Invalid username or password")
			return
		}
	}
	return (
		<div className="md:min-w-md flex flex-col justfify-center items-center border-1 bg-violet-200 p-6 max-w-md m-auto">
			<h2 className="text-2xl font-bold">Sign In</h2>
			<form
				className="flex flex-col gap-y-6 my-8"
				onSubmit={handleSubmit}
				>
				<AuthInput type="text" placeholder="Email address" value={email} setValue={setEmail}/>
				<AuthInput type="password" placeholder="Password" value={password} setValue={setPassword}/>
				<GenericButton title="Sign In"/>
			</form>
			{error && (
				<p className="text-red-600 font-semibold text-center">{error}</p>
			)}
			{info && (
				<p className="text-green-600 font-semibold text-center">{info}</p>
			)}

		</div>
	)
}
