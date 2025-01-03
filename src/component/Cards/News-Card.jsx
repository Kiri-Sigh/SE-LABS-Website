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
  fullData,
}) => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  let isAdminPage = useSelector((state) => state.mainSlice.isAdminPage);
  let relatedTopic;
  if (type === "News") {
    relatedTopic =
      related_laboratory?.related_publication ||
      related_laboratory?.related_research ||
      related_laboratory ||
      null;
  } else if (type === "Publication") {
    relatedTopic = null;
  } else if (type === "Laboratory") {
    relatedTopic = null;
  } else if (type === "Research") {
    relatedTopic = related_laboratory;
  } else {
    relatedTopic = "something wrong";
  }
  // console.log(

  const { data, isLoading, isError } = useQueryGetImg(
    `http://127.0.0.1:8000/user`,
    type,
    ID
  );

  const [imgSmall, setImgSmall] = React.useState(kmitl_logo);

  React.useEffect(() => {
    const fetchImgSmall = async () => {
      if (relatedTopic) {
        const id = relatedTopic.PID || relatedTopic.RID || relatedTopic.LID;
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
    else {
      console.log("Dispatching openSpecificModal with:", [type, ID]);
      dispatch(editAction.openSpecificModal([type, ID, fullData]));
      console.log("OpenSpecificModal", [type, ID, fullData]);
    }
  };

  const handlePublicationLink = () => {
    window.location.href = "https://www.se.kmitl.ac.th/"; // Navigates to Google
  };

  const handleSmallDivClick = (e) => {
    e.stopPropagation(); // Prevents the card click event from triggering
    // const type2 = toString(type);
    if (isAdminPage)
      dispatch(editAction.openSpecificModal([type, ID, fullData]));
    else if (relatedTopic.PID) {
      handlePublicationLink();
    } else {
      navigate(
        `/${
          relatedTopic.LID
            ? "laboratory"
            : relatedTopic.RID
            ? "research"
            : "error"
        }/${relatedTopic?.LID || relatedTopic?.RID}`
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
    type === "Laboratory"
      ? "h-[325px]"
      : type === "Publication"
      ? "h-[350px]"
      : type === "Research"
      ? "h-[350px]"
      : "h-[375px]";

  return (
    <article
      className={`flex flex-col rounded-3xl border border-black border-solid w-[250px] min-w-[250px] max-w-[250px] ${cardHeight} cursor-pointer overflow-hidden hover:shadow-lg transition-shadow duration-300`}
      onClick={
        isAdminPage
          ? handleCardClick
          : publicationLink
          ? handlePublicationLink
          : handleCardClick
      }
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
          <p className="mt-2 text-sm leading-5 line-clamp-3">{body}</p>
        </div>
        {!(isLoading && isError) && relatedTopic !== null ? (
          <div
            className="flex gap-4 items-center mt-auto w-full text-sm"
            onClick={
              publicationLink ? handlePublicationLink : handleSmallDivClick
            }
          >
            <img
              loading="lazy"
              src={imgSmall}
              alt={`${title} avatar`}
              className="shrink-0 self-stretch my-auto w-8 h-8 rounded-full object-cover"
            />
            <div className="flex flex-col flex-1 shrink self-stretch my-auto basis-0 min-w-[120px]">
              <div className="font-semibold text-gray-800 line-clamp-2">
                {relatedTopic?.title}
              </div>
              {type === "News" && (
                <div className="text-gray-600">{formattedDate}</div>
              )}
            </div>
          </div>
        ) : (
          (type === "News" || type === "Research") && (
            <div
              className="flex gap-4 items-center mt-auto w-full text-sm"
              onClick={() => (window.location.href = "http://localhost:3000/")}
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
                  <div className="text-gray-600">{formattedDate}</div>
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
