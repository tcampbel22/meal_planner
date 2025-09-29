import React, { useState } from "react";
import { GenericButton } from "./ButtonUtils";
import { useNavigate } from "react-router-dom";
import  AuthInput  from "./Utils"
import { useAuth } from "./Auth";


export const Login:React.FC = () => {
	const [email, setEmail] = useState<string>("")
	const [password, setPassword] = useState<string>("")
	const [error, setError] = useState<string | null>("")
	const [info, setInfo] = useState<string | null>("")
	const [isSubmitting, setIsSubmitting] = useState<boolean>(false)

	const navigate = useNavigate();
	const { login, isLoggedIn } = useAuth();

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();

		setError("");
  		setInfo("");

		setTimeout(() => {
			setError("");
			setInfo("")
		}, 3000)
		if (!email || !password) {
			setError("Email or password is empty")
			return
		}
		if (isLoggedIn || isSubmitting) {
			return
		}
		setIsSubmitting(true)
		try {
			await login(email, password)
			console.log("Login successful!")
			setInfo(`Login successful!`)
			setTimeout(() => {
				setEmail("")
				setPassword("")
				navigate("/hub")
			}, 1000)

		} catch (loginError: any) {
			setError(loginError.message)
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
				<GenericButton title={!isSubmitting ? "Sign In" : "Signing In"}/>
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
