import React from "react";
import { Route, Routes } from "react-router-dom";
import { HomePage } from "./Homepage";
import { Login } from "./Login";
import { NotFound } from "./NotFound";

export const AppRoutes:React.FC = () => {
	return (
		<Routes>
			<Route path="/" element={<HomePage />}/>
			<Route path="/login" element={<Login />} />
			<Route path="*" element={<NotFound />} />
			{/* <Route path="/login" element={<Register />} /> */}
		</Routes>
	)
}
