import React from "react";
import kmitl_logo from "../../../resource/kmitl_logo.webp";
import Spinner1 from "../spinner";
import "./Topic-And-Image.css";

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
            <div className="flex flex-col w-full max-md:max-w-full items-center">
                <div className="flex flex-col w-full mt-10 max-md:mt-10 max-md:max-w-full px-0">
                    <img
                        loading="lazy"
                        src={isLoading2 ? kmitl_logo : image}
                        alt="AI Laboratory visual representation"
                        className="object-contain w-full max-w-[50vw] min-w-[1000px] mx-auto aspect-[2.19] max-md:max-w-full mb-12"
                    />
                </div>
                <div className="w-3/4 flex flex-col max-md:max-w-full max-md:text-4xl items-start">
                    <h1 className="text-5xl leading-tight text-black text-center mt-5 mb-7">
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
                    <hr className="border-2 w-full self-start" />
                </div>
            </div>
        </section>
    );
};
export default TopicAndImage;
