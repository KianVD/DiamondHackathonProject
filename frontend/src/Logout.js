import React from "react";
import { useAuth0 } from "@auth0/auth0-react";

export default function LogoutButton() {
  const { logout, isAuthenticated } = useAuth0();

  const handleLogout = () => {
    // Call the logout function
    logout({
      returnTo: window.location.origin,  // Redirect back to the homepage after logging out
    });
  };

  return (
    <>
      {isAuthenticated ? (
        <button onClick={handleLogout}>Log Out</button>
      ) : (
        <p>You are not logged in.</p>
      )}
    </>
  );
}
