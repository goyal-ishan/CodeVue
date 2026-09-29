import { useState } from 'react'
import {Routes, Route} from 'react-router-dom'
import heroImg from './assets/hero.png'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import Login from "./pages/login.jsx"
import Home from "./pages/Home.jsx"
import GetStarted from "./pages/GetStarted.jsx"
import Features from "./pages/Features.jsx"
import ForgetPassword from './components/ForgetPassword.jsx'
import VerifyOtp from "./components/VerifyOtp"
import ResetPassword from "./components/ResetPassword.jsx"
function App() {
  return(
    <>
      <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/Login" element={<Login/>} />
          <Route path="/Get Started" element={<GetStarted/>}/>
          <Route path="/Features" element={<Features/>} />
          <Route path="/forget-password" element={<ForgetPassword/>}/>
          <Route path="/verify-otp" element={<VerifyOtp/>}/>
          <Route path="/reset-password" element={<ResetPassword/>}/>
      </Routes>
    </>
  )
}

export default App
