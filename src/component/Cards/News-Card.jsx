import React from "react";
import "./Card.css";
const NewsCard = ({ image, title, content, author, date }) => {
  return (
    <article className="flex flex-col rounded-3xl border border-black border-solid min-w-[240px] w-[390px]">
      <img
        loading="lazy"
        src={image}
        alt={title}
        className=" w-full rounded-tl-3xl rounded-tr-3xl aspect-[1.3]"
      />
      <div className="flex flex-col p-6 w-full bg-cyan-200 rounded-bl-3xl rounded-br-3xl border border-black border-solid max-md:px-5">
        <div className="flex flex-col w-full text-black">
          <h3 className="text-2xl font-bold leading-snug line-clamp-2 indent-clamp">
            {title}
          </h3>
          <p className="mt-2 text-base leading-6 line-clamp-3">{content}</p>
        </div>
        <div className="flex gap-4 items-center mt-6 w-full text-sm">
          <img
            loading="lazy"
            src="https://picsum.photos/300/200"
            alt={`${author} avatar`}
            className="object-contain shrink-0 self-stretch my-auto w-12 rounded-3xl aspect-square"
          />
          <div className="flex flex-col flex-1 shrink self-stretch my-auto basis-0 min-w-[240px]">
            <div className="font-semibold text-black">{author}</div>
            <div className="gap-2 self-stretch w-full text-black">{date}</div>
          </div>
        </div>
      </div>
    </article>
  );
};

export default NewsCard;
