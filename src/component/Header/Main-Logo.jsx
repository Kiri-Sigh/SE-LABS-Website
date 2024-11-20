import React from "react";
import logo from "../../resource/logo.png";
import { NavLink } from "react-router-dom";
import { useSelector } from "react-redux";
function Logo() {
  const isAdmin = useSelector((state) => state.mainSlice.isAdminPage);

  return (
    <div className="flex justify-center items-center self-stretch my-auto bg-white border border-black border-solid min-h-[65px] rounded-[52px] w-[107px]">
      <NavLink to={isAdmin ? "/admin" : "/"}>
        <img
          loading="lazy"
          src={logo}
          className="object-contain self-stretch my-auto aspect-[1.81] w-[101px]"
          alt="Company logo"
        />
      </NavLink>
    </div>
  );
}

export default Logo;
