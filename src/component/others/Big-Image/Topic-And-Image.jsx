import React from "react
import kmitl_logo from "../../../resource/kmitl_logo.webp";
import Spinner1 from "../spinner";
const TopicAndImage = ({
  data,
  image,
  isLoading,
  isLoading2,
  isLab = false,
}) => {
  if (data) console.log("data", data);
  let data2, data3;
  if (!isLab) {
    const firstKey = data ? Object.keys(data)[0] : null;
    if (firstKey === "Researcher") data2 = data ? data[firstKey].name : "";
    else {
      data2 = data ? data[firstKey].title : "";
    }
    if (data2) console.log("data2", data2); // Ensure data is logged
  } else {
    let secondkey = data ? Object.keys(data[0])[0] : null;
    data3 = data ? data[0][secondkey].title : "";
    if (data3) console.log("data3", data3);
  }

  return (
    <section className="flex overflow-hidden flex-col justify-center pt-10 w-full bg-gray-100 max-md:px-5 max-md:py-24 max-md:max-w-full">
      <div className="flex flex-col w-full max-md:max-w-full">
        <h1 className="overflow-hidden w-full text-5xl font-bold leading-tight text-black max-md:max-w-full max-md:text-4xl">
          {isLoading ? (
            <>
              loading...
              <Spinner1 />
            </>
          ) : isLab ? (
            data3
          ) : (
            data2
          )}
        </h1>
        <div className="flex flex-col w-full -mt-10 max-md:mt-10 max-md:max-w-full">
          <img
            loading="lazy"
            src={isLoading2 ? kmitl_logo : image}
            alt="AI Laboratory visual representation"
            className="object-contain w-full aspect-[2.19] max-md:max-w-full"
          />
        </div>
      </div>
    </section>
  );
};
export default TopicAndImage;
