import React from "react";
import { useLocation } from "react-router-dom";
import MainNavigation from "./MainNavigation";
import Logo from "./Main-Logo";
import "./header.css";
import OverlayButton from "component/admin-Component/overlay";

function Header() {
  const location = useLocation();

  // Check if the path is /admin
  const isAdminPage = location.pathname.startsWith("/admin");

  return (
    <>
      <header
        className={` sticky-header flex flex-col justify-center px-16 w-full min-h-[72px] max-md:px-5 max-md:max-w-full ${
          isAdminPage ? "bg-black" : "bg-blue-900"
        }`}
      >
        <div
          className={` flex flex-col justify-center px-16 w-full min-h-[72px] max-md:px-5 max-md:max-w-full ${
            isAdminPage ? "bg-black" : "bg-blue-900"
          }`}
        >
          <div className="flex flex-wrap gap-10 justify-between items-center w-full max-md:max-w-full">
            <Logo />
            <MainNavigation />
          </div>
        </div>
        {/* <OverlayButton /> */}
      </header>

      {/* Fixed Button */}
    </>
  );
}

export default Header;
