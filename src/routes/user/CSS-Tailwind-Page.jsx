import React, { useRef } from "react";
import previous from "../../resource/previous-button.svg";
import next from "../../resource/next-button.svg";

const mockTeamMembers = [
    { id: 1, name: "John Doe", email: "john.doe@example.com" },
    { id: 2, name: "Jane Smith", email: "jane.smith@example.com" },
    { id: 3, name: "Michael Johnson", email: "michael.johnson@example.com" },
    { id: 4, name: "Emily Davis", email: "emily.davis@example.com" },
    { id: 5, name: "David Wilson", email: "david.wilson@example.com" },
    { id: 6, name: "Sophia Brown", email: "sophia.brown@example.com" },
    { id: 7, name: "James Taylor", email: "james.taylor@example.com" },
];

const TeamCard = ({ name, email }) => {
    return (
        <div className="flex flex-col w-full p-6 bg-white shadow-lg rounded-lg overflow-hidden">
            <div className="text-xl font-semibold text-gray-800 truncate">
                {name}
            </div>
            <div className="flex gap-4 items-center mt-4 text-sm text-gray-600">
                <img
                    loading="lazy"
                    src="https://w7.pngwing.com/pngs/712/520/png-transparent-google-mail-gmail-logo-icon.png"
                    alt="Email icon"
                    className="object-contain w-8 h-8 rounded-full"
                />
                <div className="truncate">{email}</div>
            </div>
        </div>
    );
};

const OurTeam = () => {
    const scrollRef = useRef(null);

    const scrollLeft = () => {
        if (scrollRef.current) {
            scrollRef.current.scrollBy({ left: -300, behavior: "smooth" });
        }
    };

    const scrollRight = () => {
        if (scrollRef.current) {
            scrollRef.current.scrollBy({ left: 300, behavior: "smooth" });
        }
    };

    return (
        <section className="flex flex-col px-8 py-16 bg-gray-100">
            <div className="flex flex-wrap justify-between items-end mb-12">
                <div className="text-center w-full mb-8">
                    <h2 className="text-4xl font-bold text-gray-800">
                        Our Team
                    </h2>
                    <p className="mt-4 text-lg text-gray-600">
                        Meet our dedicated team members who make everything
                        possible.
                    </p>
                </div>
                <button className="px-6 py-2 bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700">
                    View all
                </button>
            </div>
            <div className="relative">
                <button
                    onClick={scrollLeft}
                    className="absolute left-0 top-1/2 transform -translate-y-1/2 bg-white p-2 rounded-full shadow-md hover:bg-gray-200"
                >
                    <img src={previous} alt="Previous" className="w-6 h-6" />
                </button>
                <div
                    ref={scrollRef}
                    className="flex overflow-x-auto space-x-4 p-4"
                >
                    {mockTeamMembers.map((member) => (
                        <div key={member.id} className="flex-shrink-0 w-64">
                            <TeamCard name={member.name} email={member.email} />
                        </div>
                    ))}
                </div>
                <button
                    onClick={scrollRight}
                    className="absolute right-0 top-1/2 transform -translate-y-1/2 bg-white p-2 rounded-full shadow-md hover:bg-gray-200"
                >
                    <img src={next} alt="Next" className="w-6 h-6" />
                </button>
            </div>
        </section>
    );
};

export default OurTeam;
