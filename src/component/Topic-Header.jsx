import React from "react";

function TopicHeaderText({ topic }) {
    return (
        <section className="flex overflow-hidden flex-col items-center py-28 pr-11 pl-12 w-full bg-gray-100 max-md:px-5 max-md:py-24 max-md:max-w-full">
            <div className="flex flex-col max-w-full text-center text-black w-[768px]">
                <h1 className="text-6xl font-bold leading-tight max-md:max-w-full max-md:text-4xl">
                    {topic}
                </h1>
            </div>
        </section>
    );
}

export default TopicHeaderText;
