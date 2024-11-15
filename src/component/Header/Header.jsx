import MainNavigation from "./MainNavigation";
import React from "react";
import Logo from "./Main-Logo";
import "./header.css";
function Header() {
  return (
    <header className="sticky-header flex flex-col justify-center px-16 w-full bg-blue-900 min-h-[72px] max-md:px-5 max-md:max-w-full">
      <div className="flex flex-wrap gap-10 justify-between items-center w-full max-md:max-w-full">
        <Logo />
        <MainNavigation />
      </div>
    </header>
  );
}
export default Header;
