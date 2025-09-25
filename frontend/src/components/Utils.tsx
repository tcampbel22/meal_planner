import React from "react";

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

export default AuthInput
