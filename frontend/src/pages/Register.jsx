import { Link } from "react-router-dom";

function Register() {
  return (
    <section className="panel">
      <p className="eyebrow">Get started</p>
      <h1>Create your account</h1>
      <p>Registration API integration is coming soon. Use the login page if you already have credentials.</p>
      <div className="hero-actions"><Link className="btn" to="/">Back to login</Link></div>
    </section>
  );
}

export default Register;
