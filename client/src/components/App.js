import React, { useEffect, useState } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import NavBar from "./NavBar";
import Homepage from "./Homepage";
import About from "./About";

function App() {
  return (
    <>
      <NavBar />
      <main>
        <Routes>
          <Route path="/" element={<Navigate to="/homepage" replace />} />
          <Route path="/homepage" element={<Homepage />} />
          <Route path="/about" element={<About />}/>
        </Routes>
      </main>
    </>
  );
}
export default App;

