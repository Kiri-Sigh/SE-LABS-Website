import React from "react";
import locate from "../../resource/location.svg";
import time from "../../resource/time.svg";
import { useNavigate } from "react-router-dom";

const EventCard = ({
  title,
  body,
  start,
  end,
  EID,
  related_laboratory,
  status,
  location,
}) => {
  const navigate = useNavigate();
  const handleCardClick = () => {
    navigate(`/event/${EID}`);
  };
  return (
    <div
      className="flex flex-col justify-center p-6 w-full bg-white shadow-lg rounded-lg border border-gray-200 max-md:px-4 mb-6 hover:shadow-2xl transition-shadow duration-300 cursor-pointer"
      onClick={handleCardClick}
    >
      <div className="flex flex-col w-full max-md:max-w-full">
        <div className="flex flex-wrap gap-4 items-center w-full">
          <h3 className="flex-1 text-xl font-semibold text-gray-900">
            {title}
          </h3>
          <span
            className={`px-2 py-1 text-sm font-medium text-white rounded-full ${
              status === "Coming"
                ? "bg-green-500"
                : status === "On Going"
                ? "bg-yellow-500"
                : "bg-red-500"
            }`}
          >
            {status}
          </span>
        </div>
        <p className="mt-2 text-sm text-gray-700 line-clamp-3 max-w-2xl">
          {body}
        </p>
        <div className="flex flex-wrap gap-4 items-center mt-4 text-sm text-gray-600">
          <div className="flex gap-2 items-center">
            <img loading="lazy" src={locate} alt="" className="w-5 h-5" />
            <span>{location}</span>
          </div>
          <div className="flex gap-2 items-center">
            <img loading="lazy" src={time} alt="" className="w-5 h-5" />
            <span>
              {start}-{end}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EventCard;
