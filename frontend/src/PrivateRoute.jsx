import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

function PrivateRoute({ children }) {
  const navigate = useNavigate();
  const [isAuthenticated, setIsAuthenticated] = useState(null);

  useEffect(() => {
    const user = localStorage.getItem("user"); 

    if (!user) {
      navigate("/", { replace: true });
    } else {
      setIsAuthenticated(true);
    }
  }, [navigate]);

  if (isAuthenticated === null) {
    return <div>Loading...</div>;
  }

  return children;
}

export default PrivateRoute;