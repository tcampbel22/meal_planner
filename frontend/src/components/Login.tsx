import React, { useState } from "react";
import { GenericButton } from "./ButtonUtils";
import axios from "axios";
import { useNavigate } from "react-router-dom";

type AuthInputProps = {
	type: string;
	placeholder: string;
	value: string;
	setValue: (value: string) => void;
}

const AuthInput:React.FC<AuthInputProps> = ({ type, placeholder, value, setValue }) => {
	return (
		<input
			className="text-lg border border-1 bg-violet-100 rounded-sm pl-2 py-3"
			type={type}
			placeholder={placeholder}
			value={value}
			onChange={(e) => setValue(e.target.value)}
		/>
	)
}


export const Login:React.FC = () => {
	const [email, setEmail] = useState<string>("")
	const [password, setPassword] = useState<string>("")
	const [error, setError] = useState<string | null>("")
	const navigate = useNavigate();

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setTimeout(() => {
			setError("");
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
			const response = await axios.post("http://localhost:8000/api/login", loginPayload);
			console.log("Login successful: ", response.data)
			navigate('/hub')
		} catch (error: any) {
			console.error("Error: ", error.message)
			setError("Invalid username or password")
			return
		}
		setEmail("")
		setPassword("")
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

		</div>
	)
}
