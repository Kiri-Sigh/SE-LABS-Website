import React from "react";

function SocialLinks() {
  const socialLinks = [
    {
      name: "Facebook",
      icon: "facebook-icon.svg",
      url: "https://facebook.com",
    },
    {
      name: "LinkedIn",
      icon: "linkedin-icon.svg",
      url: "https://linkedin.com",
    },
    { name: "Twitter", icon: "twitter-icon.svg", url: "https://twitter.com" },
  ];

  return (
    <nav className="flex overflow-hidden flex-1 shrink gap-6 items-start text-base font-semibold text-black basis-0 min-w-[240px]">
      <ul className="flex flex-row flex-1 shrink w-full basis-0 min-w-[240px] list-none p-0">
        {socialLinks.map((link, index) => (
          <li key={index} className={index > 0 ? "ml-3" : ""}>
            <a
              href={link.url}
              target="_blank"
              rel="noopener noreferrer"
              aria-label={`Visit our ${link.name} page`}
            >
              <img
                src={link.icon}
                alt={`${link.name} icon`}
                className="w-8 h-8"
              />
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}

export default SocialLinks;
