import React from "react";
import "./Card.css";
import kmitl_logo from "../../resource/kmitl_logo.webp";
import logo from "../../resource/logo.png";
import { getImgData } from "../../api/api-method";
import { useQueryGetImg } from "../../api/custom-hooks";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { editAction } from "store/edit-slice";

const NewsCard = ({
    title,
    body,
    date,
    ID,
    related_laboratory,
    type,
    publicationLink,
}) => {
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const isAdminPage = useSelector((state) => state.mainSlice.isAdminPage);

    const relatedTopic =
        type === "News"
            ? related_laboratory?.related_publication ||
              related_laboratory?.related_research ||
              related_laboratory
            : type === "Research"
            ? related_laboratory
            : null;

    const { data, isLoading, isError } = useQueryGetImg(
        `http://127.0.0.1:8000/user`,
        type,
        ID
    );

    const [imgSmall, setImgSmall] = React.useState(kmitl_logo);

    React.useEffect(() => {
        const fetchImgSmall = async () => {
            if (relatedTopic) {
                const id =
                    relatedTopic.PID || relatedTopic.RID || relatedTopic.LID;
                const typePath = relatedTopic.PID
                    ? "publication"
                    : relatedTopic.RID
                    ? "research"
                    : "laboratory";
                const fetchedImg = await getImgData(
                    `http://127.0.0.1:8000/user/${typePath}/image-low?${typePath}_id=${id}`
                );
                setImgSmall(fetchedImg);
            }
        };
        fetchImgSmall();
    }, [relatedTopic]);

    const titleClass =
        title.length <= 20 ? "title-clamp short-title" : "title-clamp";
    const handleCardClick = () => {
        if (!isAdminPage) navigate(`/${type}/${ID}`);
        else dispatch(editAction.openModal());
    };
    const handlePublicationLink = () => {
        window.location.href = "https://www.se.kmitl.ac.th/";
    };
    const handleSmallDivClick = (e) => {
        e.stopPropagation();
        if (relatedTopic.PID) {
            handlePublicationLink();
        } else {
            navigate(
                `/${relatedTopic.LID ? "laboratory" : "research"}/${
                    relatedTopic?.LID || relatedTopic?.RID
                }`
            );
        }
    };
    const formattedDate = new Date(date).toLocaleString("en-US", {
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        hour12: true,
    });
    const cardHeight =
        type === "Laboratory" || type === "Publication"
            ? "h-[325px]"
            : type === "Research"
            ? "h-[350px]"
            : "h-[375px]";

    return (
        <article
            className={`flex flex-col rounded-3xl border border-black border-solid min-w-[240px] w-[325px] ${cardHeight} cursor-pointer overflow-hidden hover:shadow-lg transition-shadow duration-300`}
            onClick={publicationLink ? handlePublicationLink : handleCardClick}
        >
            <div className="relative">
                <img
                    loading="lazy"
                    src={isLoading ? kmitl_logo : data}
                    alt={title}
                    className="w-full h-[150px] rounded-tl-3xl rounded-tr-3xl object-cover"
                />
            </div>
            <div className="flex flex-col p-4 w-full bg-white flex-1 rounded-bl-3xl rounded-br-3xl">
                <div className="flex flex-col w-full text-gray-800 flex-1">
                    <h3
                        className={`text-xl font-bold leading-snug line-clamp-2 indent-clamp ${titleClass}`}
                    >
                        {title}
                        {title.length <= 20 ? <br /> : null}
                    </h3>
                    <p className="mt-2 text-sm leading-5 line-clamp-3">
                        {body}
                    </p>
                </div>
                {!(isLoading && isError) && relatedTopic !== null ? (
                    <div
                        className="flex gap-4 items-center mt-auto w-full text-sm"
                        onClick={
                            publicationLink
                                ? handlePublicationLink
                                : handleSmallDivClick
                        }
                    >
                        <img
                            loading="lazy"
                            src={imgSmall}
                            alt={`${title} avatar`}
                            className="object-contain shrink-0 self-stretch my-auto w-8 h-8 rounded-full"
                        />
                        <div className="flex flex-col flex-1 shrink self-stretch my-auto basis-0 min-w-[120px]">
                            <div className="font-semibold text-gray-800 line-clamp-2">
                                {relatedTopic?.title}
                            </div>
                            {type !== "Research" && (
                                <div className="text-gray-600">
                                    {formattedDate}
                                </div>
                            )}
                        </div>
                    </div>
                ) : (
                    (type === "News" || type === "Research") && (
                        <div
                            className="flex gap-4 items-center mt-auto w-full text-sm"
                            onClick={() =>
                                (window.location.href =
                                    "http://localhost:3000/")
                            }
                        >
                            <img
                                loading="lazy"
                                src={type === "Research" ? imgSmall : logo}
                                alt={`${title} avatar`}
                                className="object-contain shrink-0 self-stretch my-auto w-8 h-8 rounded-full"
                            />
                            <div className="flex flex-col flex-1 shrink self-stretch my-auto basis-0 min-w-[120px]">
                                <div className="font-semibold text-gray-800 line-clamp-2">
                                    {type === "Research"
                                        ? relatedTopic?.title
                                        : "KMITL Software engineering department"}
                                </div>
                                {type === "News" && (
                                    <div className="text-gray-600">
                                        {formattedDate}
                                    </div>
                                )}
                            </div>
                        </div>
                    )
                )}
            </div>
        </article>
    );
};

export default NewsCard;
