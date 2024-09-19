import logo from "../../resources/logo.png";
function Logo() {
  return (
    <div className="flex justify-center items-center self-stretch my-auto bg-white border border-black border-solid min-h-[65px] rounded-[52px] w-[107px]">
      <img
        loading="lazy"
        src={logo}
        className="object-contain self-stretch my-auto aspect-[1.81] w-[101px]"
        alt="Company logo"
      />
    </div>
  );
}

export default Logo;
