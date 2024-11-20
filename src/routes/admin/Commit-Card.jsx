import React from "react";
import "component/Cards/Card.css";
import kmitl_logo from "../../resource/kmitl_logo.webp";
import { getData, getImgData } from "../../api/api-method";
import { useNormalQueryGet, useQueryGetImg } from "../../api/custom-hooks";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { editAction } from "store/edit-slice";

const CommitCard = ({
  title,
  body,
  date,
  ID,
  related_laboratory,
  type,
  publicationLink,
  fullData,
}) => {
  // console.log(title);
  const navigate = useNavigate();
  const dispatch = useDispatch();
  let isAdminPage = useSelector((state) => state.mainSlice.isAdminPage);
  let relatedTopic;
  //   if (type === "News") {
  //     relatedTopic =
  //       related_laboratory?.related_publication ||
  //       related_laboratory?.related_research ||
  //       related_laboratory ||
  //       null;
  //   } else if (type === "Publication") {
  //     relatedTopic = null;
  //   } else if (type === "Laboratory") {
  //     relatedTopic = null;
  //   } else if (type === "Research") {
  //     relatedTopic = related_laboratory;
  //   } else {
  //     relatedTopic = "something wrong";
  //   }
  // console.log(relatedTopic);

  // const [image, setImage] = React.useState(kmitl_logo);
  //   const [imgSmall, setImgSmall] = React.useState(kmitl_logo);

  // React.useEffect(() => {
  //   const fetchImage = async () => {
  //     const fetchedImage = await getData(
  //       `http://127.0.0.1:8000/user/news/image-high?news_id=${NID}`
  //     );
  //     setImage(fetchedImage);
  //   };
  //   fetchImage();
  // }, [NID]);

  //   React.useEffect(() => {
  //     const fetchImgSmall = async () => {

  //       if (relatedTopic) {
  //         if (relatedTopic.PID) {
  //           const fetchedImg = await getImgData(
  //             `http://127.0.0.1:8000/user/publication/image-low?publication_id=${relatedTopic.PID}`
  //           );
  //           setImgSmall(fetchedImg);
  //         } else if (relatedTopic.RID) {
  //           const fetchedImg = await getImgData(
  //             `http://127.0.0.1:8000/user/research/image-low?research_id=${relatedTopic.RID}`
  //           );
  //           setImgSmall(fetchedImg);
  //         } else if (relatedTopic.LID) {
  //           const fetchedImg = await getImgData(
  //             `http://127.0.0.1:8000/user/laboratory/image-low?laboratory_id=${relatedTopic.LID}`
  //           );
  //           setImgSmall(fetchedImg);
  //         }
  //       }
  //     };
  //     fetchImgSmall();
  //   }, [relatedTopic]);
  const titleClass =
    title.length <= 20 ? "title-clamp short-title" : "title-clamp";
  const handleCardClick = () => {
    if (!isAdminPage) navigate(`/${type}/${ID}`);
    else {
      console.log("Dispatching openSpecificModal with:", [type, ID]);
      dispatch(editAction.openSpecificModal([type, ID, fullData]));
      dispatch(editAction.isCommit(true));
    }
  };
  //   const handlePublicationLink = () => {
  //     window.location.href = "https://www.se.kmitl.ac.th/"; // Navigates to Google
  //   };
  const handleSmallDivClick = (e) => {
    e.stopPropagation(); // Prevents the card click event from triggering
    // const type2 = toString(type);
    // if (relatedTopic.PID) {
    //   handlePublicationLink();
    // } else {
    //   navigate(
    //     `/${
    //       relatedTopic.LID
    //         ? "laboratory"
    //         : relatedTopic.RID
    //         ? "research"
    //         : "error"
    //     }/${relatedTopic?.LID || relatedTopic?.RID}`
    //   );
    // }
  };
  return (
    <article
      className="flex flex-col rounded-3xl border border-black border-solid min-w-[240px] w-[325px]"
      onClick={handleCardClick}
    >
      <div className="relative">
        <img
          loading="lazy"
          src={kmitl_logo}
          alt={title}
          className="w-full rounded-tl-3xl rounded-tr-3xl aspect-[1.3]"
        />
        {/* <button className="absolute top-2 right-2 bg-blue-500 text-white px-4 py-2 rounded-full hover:bg-blue-600 transition">
          Edit
        </button> */}
      </div>
      <div className="flex flex-col p-6 w-full bg-cyan-200 rounded-bl-3xl rounded-br-3xl border border-black border-solid max-md:px-5">
        <div className="flex flex-col w-full text-black">
          <h3
            className={`text-2xl font-bold leading-snug line-clamp-2 indent-clamp ${titleClass}`}
          >
            {title}
            {title.length <= 20 ? <br /> : null}
          </h3>
          <p className="mt-2 text-base leading-6 line-clamp-3">{body}</p>
        </div>
      </div>
    </article>
  );
};

export default CommitCard;
