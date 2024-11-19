import Header from "component/Header/Header";
import MainNavigation from "component/Header/MainNavigation";
import { Outlet, useNavigation } from "react-router-dom";
// import MainNavigation from "../../component/MainNavigation";

function AdminLayout() {
  // const navigation = useNavigation();

  return (
    <>
      <Header />
      <main>
        <Outlet />
      </main>
    </>
  );
}

export default AdminLayout;
