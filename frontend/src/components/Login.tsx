import React, { useState } from "react";
import { HeaderButton } from "./HeaderButton";

type AuthInputProps = {
	type: string;
	placeholder: string;
	value: string;
	setValue: (value: string) => void;
}

const AuthInput:React.FC<AuthInputProps> = ({ type, placeholder, value, setValue }) => {
	return (
		<input
			className="text-lg border border-1 bg-violet-100 rounded-sm pl-2 py-3 my-4"
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

	return (
		<div className="flex flex-col justfify-center items-center border-1 bg-violet-200 p-6 max-w-md m-auto">
			<h2 className="text-2xl font-bold">Sign In</h2>
			<AuthInput type="text" placeholder="Email address" value={email} setValue={setEmail}/>
			<AuthInput type="text" placeholder="Password" value={password} setValue={setPassword}/>
			<HeaderButton title="Sign In" link="/hub"/>
		</div>
	)
}
