import React, { Suspense, useContext } from "react";
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import { UserContext } from "./context/UserContext.js";
import ScrollToTop from "./ScrollToTop";

// CORE
const Home = React.lazy(() => import("./pages/Core/Home/Index"));


// ACCOUNTS
const Login = React.lazy(() => import("./pages/Accounts/Login/Index.js"));
const Register = React.lazy(() => import("./pages/Accounts/Register/Index.js"));
const ResetPassword = React.lazy(() =>
  import("./pages/Accounts/ForgetPassword/Index.js")
);

// UserPanel
const Panel = React.lazy(() => import("./pages/Panel/Home/Index.js"));

// Admin Panel
const Admin = React.lazy(() => import("./pages/Admin/Home/Index.js"));


function App() {
  const authCtx = useContext(UserContext);
  return (
    <Suspense fallback={""}>
      <BrowserRouter>
        <ScrollToTop />
        <Routes>
          {/* CORE */}
          <Route index element={<Home />} />
        
          {/* Accounts */}
          <Route path="/zaloguj-sie" element={<Login />} />
          <Route path="/zarejestruj-sie" element={<Register />} />
          <Route path="/przypomnij-haslo" element={<ResetPassword />} />

          {authCtx.isLoggedIn && (
            <>
              <Route path="/moje-konto" element={<Panel />} />
              
              {/* ADMIN */}

              <Route path="/admin" element={<Admin />} />
            </>
          )}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </BrowserRouter>
    </Suspense>
  );
}

export default App;