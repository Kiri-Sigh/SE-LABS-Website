import { Outlet, useNavigation } from "react-router-dom";
import Footer from "../../component/Footer/footer";
import Header from "../../component/Header.jsx/Header";
import backgroundImage from "../../resources/background.webp";
function RootLayout() {
  // const navigation = useNavigation();

  return (
    <>
      <div
        style={{ backgroundImage: `url(${backgroundImage})` }}
        className="hero"
      >
        <Header />

        {/* {navigation.state === 'loading' && <p>Loading...</p>} */}

        <Outlet className="content" />

        <Footer />
      </div>
    </>
  );
}

export default RootLayout;
