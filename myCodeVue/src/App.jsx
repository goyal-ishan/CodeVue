import { useState } from 'react'
import {Routes, Route} from 'react-router-dom'
import heroImg from './assets/hero.png'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import Login from "./pages/Login.jsx"
import Home from "./pages/Home.jsx"
import GetStarted from "./pages/GetStarted.jsx"
import Features from "./pages/Features.jsx"



function App() {
  return(
    <>
      <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/Login" element={<Login/>} />
          <Route path="/Get Started" element={<GetStarted/>}/>
          <Route path="/Features" element={<Features/>} />
      </Routes>
    </>
  )
}

export default App
