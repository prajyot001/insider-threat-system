import Lottie from "lottie-react";
import animationData from "../assets/security-animation.json";
import "../styles/login.css";

function AuthLayout({ children }) {
  return (
    <div className="login-container">
      
      <div className="left-panel">
        <Lottie
          animationData={animationData}
          loop={true}
        />
      </div>

      <div className="right-panel">
        <div className="login-box">
          {children}
        </div>
      </div>

    </div>
  );
}

export default AuthLayout;