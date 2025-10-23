import React, { useState } from "react";
import { GenericButton } from "./ButtonUtils";
import axios, { AxiosError } from "axios";
import { useNavigate } from "react-router-dom";
import { GenericInput } from "./Utils";

const API_URL = import.meta.env.VITE_API_URL

export const Register:React.FC = () => {
	const [username, setUsername] = useState<string>("")
	const [email, setEmail] = useState<string>("")
	const [password, setPassword] = useState<string>("")
	const [passwordCheck, setPasswordCheck] = useState<string>("")
	const [error, setError] = useState<string | null>("")
	const [info, setInfo] = useState<string | null>("")
	const navigate = useNavigate()

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault()
		setTimeout(() => {
			setError("")
			setInfo("")
		}, 3000)
		try {
			if (!email || !password || !passwordCheck || !username) {
				setError("Missing field: All fields required")
				return
			}
			if (password != passwordCheck) {
				setError("Passwords do not match")
				return
			}
			const registerPayload = {
				email,
				username,
				password
			}
			const response = await axios.post(`${API_URL}/users/`, registerPayload)
			console.log(`Registration successful for ${response.data.username}`)
			setInfo("Registration successful!")
			setEmail("")
			setUsername("")
			setPassword("")
			setPasswordCheck("")
			setTimeout(() => {
				navigate("/login")
			}, 2000)

		} catch (error: unknown) {
			if (axios.isAxiosError(error)) {
				const axiosError = error as AxiosError;
				if (axiosError.response?.status == 409)
					setError("Username or email already exists")
				else if (axiosError.response?.status == 422)
					setError("Invalid email, password or username format")
				else
					setError("Registration failed, please try again")
			} else {
				setError("Registration failed")
			}
			console.error(`Registration failed: ${error}`)
			return
		}
	}

	return (
		<div className="md:min-w-md flex flex-col items-center border-1 bg-violet-200 p-6 max-w-md m-auto my-4">
			<h2 className="text-2xl font-bold">Register</h2>
			<form
				className="flex flex-col gap-y-6 my-8"
				onSubmit={handleSubmit}
				>
				<GenericInput type="email" placeholder="Email address" value={email} setValue={setEmail}/>
				<GenericInput type="username" placeholder="username" value={username} setValue={setUsername}/>
				<GenericInput type="password" placeholder="Password" value={password} setValue={setPassword}/>
				<GenericInput type="password" placeholder="Retype password" value={passwordCheck} setValue={setPasswordCheck}/>
				<GenericButton title="Register"/>
			</form>
			{error && (
				<p className="text-red-600 font-semibold text-center">{error}</p>
			)}
			{info && (
				<p className="text-green-400 font-semibold text-center">{info}</p>
			)}

		</div>
	)
}
