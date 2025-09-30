import React from "react";

type GenericInputProps = {
	type: string;
	placeholder: string;
	value: string;
	setValue: (value: string) => void;
}

const GenericInput:React.FC<GenericInputProps> = ({ type, placeholder, value, setValue }) => {
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

export default GenericInput
