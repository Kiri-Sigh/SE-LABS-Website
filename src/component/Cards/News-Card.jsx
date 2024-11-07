import React from "react";
import "./Card.css";
import kmitl_logo from "../../resource/kmitl_logo.webp";
import { getData, getImgData } from "../../api/api-method";
import { useNormalQueryGet, useQueryGetImg } from "../../api/custom-hooks";
const NewsCard = ({ title, body, date, NID, related_laboratory }) => {
  console.log(title);
  const relatedTopic =
    related_laboratory.related_publication ||
    related_laboratory.related_research ||
    related_laboratory ||
    null;
  const { data, isLoading } = useQueryGetImg(
    `http://127.0.0.1:8000/user/news/image-high?news_id=${NID}`,
    "news",
    NID
  );

  // const [image, setImage] = React.useState(kmitl_logo);
  const [imgSmall, setImgSmall] = React.useState(kmitl_logo);

  // React.useEffect(() => {
  //   const fetchImage = async () => {
  //     const fetchedImage = await getData(
  //       `http://127.0.0.1:8000/user/news/image-high?news_id=${NID}`
  //     );
  //     setImage(fetchedImage);
  //   };
  //   fetchImage();
  // }, [NID]);

  React.useEffect(() => {
    const fetchImgSmall = async () => {
      // if (relatedTopic.PID) {
      //   const fetchedImg = await getData(
      //     `http://127.0.0.1:8000/user/publication/image-low?publication_id=${relatedTopic.PID}`
      //   );
      //   setImgSmall(fetchedImg);
      // } else if (relatedTopic.RID) {
      //   const fetchedImg = await getData(
      //     `http://127.0.0.1:8000/user/publication/image-low?research_id=${relatedTopic.RID}`
      //   );
      //   setImgSmall(fetchedImg);
      // } else if (relatedTopic) {
      //   const fetchedImg = await getData(
      //     `http://127.0.0.1:8000/user/publication/image-low?laboratory_id=${relatedTopic}`
      //   );
      //   setImgSmall(fetchedImg);
      // }
      if (relatedTopic.PID) {
        const fetchedImg = await getImgData(
          `http://127.0.0.1:8000/user/publication/image-low?publication_id=${relatedTopic.PID}`
        );
        setImgSmall(fetchedImg);
      } else if (relatedTopic.RID) {
        const fetchedImg = await getImgData(
          `http://127.0.0.1:8000/user/publication/image-low?publication_id=${relatedTopic.RID}`
        );
        setImgSmall(fetchedImg);
      } else if (relatedTopic.LID) {
        const fetchedImg = await getImgData(
          `http://127.0.0.1:8000/user/publication/image-low?publication_id=${relatedTopic.LID}`
        );
        setImgSmall(fetchedImg);
      }
    };
    fetchImgSmall();
  }, [relatedTopic]);

  return (
    <article className="flex flex-col rounded-3xl border border-black border-solid min-w-[240px] w-[325px]">
      <div className="relative">
        <img
          loading="lazy"
          src={isLoading ? kmitl_logo : data}
          alt={title}
          className="w-full rounded-tl-3xl rounded-tr-3xl aspect-[1.3]"
        />
        {/* Edit button overlay */}
        <button className="absolute top-2 right-2 bg-blue-500 text-white px-4 py-2 rounded-full hover:bg-blue-600 transition">
          Edit
        </button>
      </div>
      <div className="flex flex-col p-6 w-full bg-cyan-200 rounded-bl-3xl rounded-br-3xl border border-black border-solid max-md:px-5">
        <div className="flex flex-col w-full text-black">
          <h3 className="text-2xl font-bold leading-snug line-clamp-2 indent-clamp">
            {title}
          </h3>
          <p className="mt-2 text-base leading-6 line-clamp-3">{body}</p>
        </div>
        <div className="flex gap-4 items-center mt-6 w-full text-sm">
          <img
            loading="lazy"
            src={imgSmall}
            alt={`${title} avatar`}
            className="object-contain shrink-0 self-stretch my-auto w-12 rounded-3xl aspect-square"
          />
          <div className="flex flex-col flex-1 shrink self-stretch my-auto basis-0 min-w-[240px]">
            <div className="font-semibold text-black">{relatedTopic.title}</div>
            <div className="gap-2 self-stretch w-full text-black">{date}</div>
          </div>
        </div>
      </div>
    </article>
  );
};

export default NewsCard;
