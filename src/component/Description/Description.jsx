import Spinner1 from "component/others/spinner";
import React from "react";

const Description = ({ data, isLab, isLoading }) => {
    if (data) console.log("data", data);
    let data2, data3, isResearcher;
    if (!isLab) {
        const firstKey = data ? Object.keys(data)[0] : null;
        if (firstKey === "Researcher") {
            data2 = data ? data[firstKey].gmail : "";
            isResearcher = true;
        } else {
            data2 = data ? data[firstKey].body : "";
        }
        if (data2) console.log("data2", data2); // Ensure data is logged
    } else {
        let secondkey = data ? Object.keys(data[0])[0] : null;
        data3 = data ? data[0][secondkey].body : "";
        if (data3) console.log("data3", data3);
    }
    return (
        <section className="flex overflow-hidden flex-col justify-center px-16 py-28 pb-16 w-full text-lg leading-6 text-black bg-gray-100 max-md:px-5 max-md:py-24 max-md:max-w-full items-center">
            <div
                className={`flex flex-col w-3/4 max-md:max-w-3/4 mx-auto mb-32 ${
                    isResearcher ? "text-center" : ""
                }`}
            >
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
            </div>
            <hr className="border-2 w-5/6 self-center" />
        </section>
    );
};

export default Description;
