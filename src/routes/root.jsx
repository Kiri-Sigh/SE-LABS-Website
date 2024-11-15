import { Outlet, useNavigation } from "react-router-dom";
import Header from "../component/Header/Header";
import Footer from "../component/Footer/footer";
import { useDispatch } from "react-redux";
//import ThumbnailCard from "../component/etc/Thumbnail-test";
import { mainAction } from "../store/main-slice";
function RootLayout() {
  // const navigation = useNavigation();
  const dispatch = useDispatch();
  return (
    <>
      <Header />
      {/* <button onClick={() => dispatch(mainAction.isAdmin())}>-admin-</button>
      <button onClick={() => dispatch(mainAction.isLead())}>-lead-</button>
      <button onClick={() => dispatch(mainAction.isResearcher())}>
        -researcher-
      </button> */}

      <main>
        {/* {navigation.state === 'loading' && <p>Loading...</p>} */}
        <Outlet />
      </main>
      <Footer />
    </>
  );
}

export default RootLayout;
