import React from "react";
import "./Card.css";
import kmitl_logo from "../../resource/kmitl_logo.webp";
import { getData, getImgData } from "../../api/api-method";
import { useNormalQueryGet, useQueryGetImg } from "../../api/custom-hooks";
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
  // console.log(title);
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

  const { data, isLoading, isError } = useQueryGetImg(
    `http://127.0.0.1:8000/user`,
    type,
    ID
  );

  const [imgSmall, setImgSmall] = React.useState(kmitl_logo);

  React.useEffect(() => {
    const fetchImgSmall = async () => {
      if (relatedTopic) {
        if (relatedTopic.PID) {
          const fetchedImg = await getImgData(
            `http://127.0.0.1:8000/user/publication/image-low?publication_id=${relatedTopic.PID}`
          );
          setImgSmall(fetchedImg);
        } else if (relatedTopic.RID) {
          const fetchedImg = await getImgData(
            `http://127.0.0.1:8000/user/research/image-low?research_id=${relatedTopic.RID}`
          );
          setImgSmall(fetchedImg);
        } else if (relatedTopic.LID) {
          const fetchedImg = await getImgData(
            `http://127.0.0.1:8000/user/laboratory/image-low?laboratory_id=${relatedTopic.LID}`
          );
          setImgSmall(fetchedImg);
        }
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
    window.location.href = "https://www.se.kmitl.ac.th/"; // Navigates to Google
  };
  const handleSmallDivClick = (e) => {
    e.stopPropagation(); // Prevents the card click event from triggering
    // const type2 = toString(type);
    if (relatedTopic.PID) {
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
  return (
    <article
      className="flex flex-col rounded-3xl border border-black border-solid min-w-[240px] w-[325px]"
      onClick={publicationLink ? handlePublicationLink : handleCardClick}
    >
      <div className="relative">
        <img
          loading="lazy"
          src={isLoading ? kmitl_logo : data}
          alt={title}
          className="w-full rounded-tl-3xl rounded-tr-3xl aspect-[1.3]"
        />
      </div>
      <div className="flex flex-col p-4 w-full bg-white flex-1">
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
              className="object-contain shrink-0 self-stretch my-auto w-10 h-10 rounded-full"
            />
            <div className="flex flex-col flex-1 shrink self-stretch my-auto basis-0 min-w-[240px]">
              <div className="font-semibold text-gray-800">
                {relatedTopic?.title}
              </div>
              <div className="text-gray-600">{date}</div>
            </div>
          </div>
        ) : null}
      </div>
    </article>
  );
};

export default NewsCard;
