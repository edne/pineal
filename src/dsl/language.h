class pFunc{
	public:
		pFunc(){}

		pFunc(py::object f){
			lambda = [f](){ f(); };
		}

		void __call__(){
			lambda();
		}

		void operator()(){
			lambda();
		}

		function<void(void)> lambda = [](){};
};
