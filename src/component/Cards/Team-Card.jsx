import React from "react";
import "./Card.css";
import { getImgData } from "api/api-method";
import kmitl_logo from "../../resource/kmitl_logo.webp";
import logo from "../../resource/logo.png";
import { useQueryGetImg } from "api/custom-hooks";
import { useNavigate } from "react-router-dom";

const TeamCard = ({
    UID,
    position,
    related_laboratory,
    related_research,
    name,
    gmail,
}) => {
    const navigate = useNavigate();
    const [imgSmall, setImgSmall] = React.useState(kmitl_logo);

    const { data, isLoading, isError } = useQueryGetImg(
        `http://127.0.0.1:8000/user`,
        "researcher",
        UID
    );

    let relatedTopic = null;

    if (related_laboratory && related_laboratory[0]?.LID) {
        relatedTopic = "laboratory";
    } else if (related_research && related_research[0]?.RID) {
        relatedTopic = "research";
    }

    const borderColor =
        {
            Admin: "border-red-500",
            "Lead-Researcher": "border-blue-500",
            Researcher: "border-green-500",
            Free: "border-gray-500",
        }[position] || "border-black";

    const handleCardClick = (e) => {
        e.stopPropagation();

        navigate(`/people/${UID}`);
    };

    React.useEffect(() => {
        const fetchImgSmall = async () => {
            if (position === "Admin") {
                setImgSmall(logo);
            } else if (relatedTopic) {
                if (relatedTopic === "laboratory") {
                    const fetchedImg = await getImgData(
                        `http://127.0.0.1:8000/user/laboratory/image-low?laboratory_id=${related_laboratory[0]?.LID}`
                    );
                    setImgSmall(fetchedImg);
                } else if (relatedTopic === "research") {
                    const fetchedImg = await getImgData(
                        `http://127.0.0.1:8000/user/research/image-low?research_id=${related_research[0]?.RID}`
                    );
                    setImgSmall(fetchedImg);
                }
            }
        };
        fetchImgSmall();
    }, [position, relatedTopic, related_laboratory, related_research]);

    const handleSmallDivClick = (e) => {
        e.stopPropagation();
        if (!relatedTopic) return;

        navigate(
            `/${
                relatedTopic === "laboratory"
                    ? "laboratory"
                    : relatedTopic === "research"
                    ? "research"
                    : "error"
            }/${related_laboratory[0]?.LID || related_laboratory[0]?.RID}`
        );
    };

    return (
        <div
            className={`flex flex-col m-5 rounded-3xl border border-black border-solid min-w-[240px] w-[275px] md:w-[275px] 2xl:w-[325px] md:h-[385px] 2xl:h-[425px] cursor-pointer shadow-lg hover:shadow-2xl transition-shadow duration-300`}
            style={{ boxSizing: "border-box" }} // Prevents border overlap
            onClick={handleCardClick}
        >
            <img
                loading="lazy"
                src={isLoading ? kmitl_logo : data}
                alt=""
                className="w-full rounded-tl-3xl rounded-tr-3xl aspect-[1.3] border-black border-b"
            />
            <div className="flex flex-col p-6 w-full bg-white rounded-none max-md:px-5 rounded-bl-3xl rounded-br-3xl h-[175px]">
                <div>{position}</div>
                <div className="flex flex-col w-full text-2xl font-bold leading-snug text-black line-clamp-2 indent-clamp">
                    <div className="w-full">{name}</div>
                </div>
                {position !== "Free" && (
                    <div className="flex flex-col gap-2 w-full text-sm font-semibold text-black">
                        <div
                            className="flex gap-4 items-center mt-2 w-full text-sm"
                            onClick={
                                !(isLoading && isError) && relatedTopic !== null
                                    ? handleSmallDivClick
                                    : undefined
                            }
                        >
                            <img
                                loading="lazy"
                                src={imgSmall}
                                alt={`${name} avatar`}
                                className="object-contain shrink-0 self-stretch my-auto w-12 rounded-3xl aspect-square"
                            />
                            <div className="flex flex-col flex-1 shrink self-stretch my-auto basis-0 min-w-[150px]">
                                <div className="font-semibold text-black line-clamp-2">
                                    {position === "Admin"
                                        ? "KMITL Software Engineering Department"
                                        : relatedTopic === "laboratory"
                                        ? related_laboratory[0]?.title
                                        : relatedTopic === "research"
                                        ? related_research[0]?.title
                                        : ""}
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default TeamCard;
