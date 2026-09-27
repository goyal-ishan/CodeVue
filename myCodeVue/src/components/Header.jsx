import { Link } from "react-router-dom";
import logo from "../assets/CodeVue Logo.png";
import HowItWorks from "./HowItWorks.jsx";

function Header() {
    return (
        <header className="Header-container">

           <div className="header-logo">
                <div className="logo-icon">
                     <span>&lt;</span>
                     <span className="greater-than">&gt;</span>
                </div>
                <div className="LogoName">
                     <span className="logo-code">Code</span>
                     <span className="logo-vue">Vue</span>
                </div>
           </div>

            <nav>
                <ul className="list-of-pages">
                    <li>
                        <Link to="/">Home</Link>
                    </li>

                    <li>
                        <a href="#how-it-works">How It Works</a>
                    </li>

                    <li>
                        <Link to="/Features">Features</Link>
                    </li>
                </ul>

                <ul className="registration">
                    <li>
                        <Link to="/Login" className="login">Login</Link>
                    </li>

                    <li>
                        <Link to="/Get Started" className="GetStartedButton">Get Started</Link>
                    </li>
                </ul>
            </nav>

        </header>

    );
}

export default Header;