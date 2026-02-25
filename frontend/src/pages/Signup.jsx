import { useState } from "react";
import { supabase } from "../services/supabaseClient";
import { useNavigate } from "react-router-dom";
import AuthLayout from "../components/AuthLayout";

function Signup() {
  const [companyName, setCompanyName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();

    const { error } = await supabase.auth.signUp({
      email,
      password,
    });

    if (error) {
      alert(error.message);
      return;
    }

    await supabase.from("companies").insert([
      {
        company_name: companyName,
        plan_type: "basic",
      },
    ]);

    alert("Account created! Please verify your email.");
    navigate("/");
  };

  return (
    <AuthLayout
      title="Create Account"
      subtitle="Register your company and start monitoring securely."
    >
      <form onSubmit={handleSignup}>
        <input
          type="text"
          placeholder="Company Name"
          onChange={(e) => setCompanyName(e.target.value)}
          required
        />

        <input
          type="email"
          placeholder="Admin Email"
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit">Create Account</button>
      </form>

      <div className="links">
        <span onClick={() => navigate("/")}>
          Already have an account? Login
        </span>
      </div>
    </AuthLayout>
  );
}

export default Signup;