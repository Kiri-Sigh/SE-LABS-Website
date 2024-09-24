import React from "react";
import { render, screen } from "@testing-library/react";
import Footer from "./footer";

describe("Footer", () => {
  test("renders contact information", () => {
    render(<Footer />);
    expect(screen.getByText("Address:")).toBeInTheDocument();
    expect(screen.getByText(/1 Chalong Krung 1 Alley/)).toBeInTheDocument();
    expect(screen.getByText("Contact:")).toBeInTheDocument();
    expect(screen.getByText("02 329 8000")).toBeInTheDocument();
    expect(screen.getByText("info@kmitl.ac.th")).toBeInTheDocument();
  });

  test("renders social media icons", () => {
    render(<Footer />);
    expect(screen.getByAltText("Facebook icon")).toBeInTheDocument();
    expect(screen.getByAltText("LinkedIn icon")).toBeInTheDocument();
    expect(screen.getByAltText("Twitter icon")).toBeInTheDocument();
  });

  test("renders company logo", () => {
    render(<Footer />);
    const logo = screen.getByAltText("Company logo");
    expect(logo).toBeInTheDocument();
    expect(logo).toHaveAttribute(
      "src",
      "https://cdn.builder.io/api/v1/image/assets/TEMP/5efedf53fa5e098141a63a5eb5e0add0b77b3820af95f07957e7aae03d04a014?placeholderIfAbsent=true&apiKey=48b4d741997c411b883c3a9cff6347e7"
    );
  });
});
