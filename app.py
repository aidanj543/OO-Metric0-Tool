import streamlit as st

from analyzer import analyze_code


# Configure the page
st.set_page_config(
    page_title="OO Metrics Analyzer",
    page_icon="📊",
    layout="wide"
)

# Page heading
st.title("OO Metrics Analyzer")


with st.expander("About the OO Metrics"):
    st.markdown("""
    **WMC — Weighted Methods per Class**
    - Counts explicitly declared methods.
    - Each method has weight 1.

    **COM — Cohesion of Methods**
    - Measures the proportion of method pairs
      sharing at least one instance attribute.
    - Range: 0.0 to 1.0.
    - Zero-method classes return 0.0.
    - One-method classes return 1.0.

    **CBO — Coupling Between Objects**
    - Counts unique referenced classes defined
      in the analyzed Python file.

    **RFC — Response for a Class**
    - Counts distinct declared method names
      and directly called attribute-method names.

    These metrics use simplified static analysis.
    """)


st.write(
    "Analyze Python class definitions using four "
    "Object-Oriented software metrics: "
    "WMC, COM, CBO, and RFC."
)

st.divider()

# Input method selection
input_method = st.radio(
    "Choose how to provide Python code:",
    ["Upload Python File", "Paste Python Code"]
)

source_code = ""

# Option 1: Upload a Python file
if input_method == "Upload Python File":

    uploaded_file = st.file_uploader(
        "Upload a .py file",
        type=["py"]
    )

    if uploaded_file is not None:
        try:
            source_code = uploaded_file.getvalue().decode(
                "utf-8-sig"
            )

            st.success(
                f"File uploaded: {uploaded_file.name}"
            )

        except UnicodeDecodeError:
            st.error(
                "Unable to read the file. "
                "Please upload a UTF-8 Python file."
            )

# Option 2: Paste Python source
else:

    source_code = st.text_area(
        "Paste your Python class definitions:",
        height=300,
        placeholder=(
            "class Student:\n"
            "    def study(self):\n"
            "        pass"
        )
    )


# Analyze button
if st.button("Analyze OO Metrics", type="primary"):

    try:
        # Run our integration module
        results = analyze_code(source_code)

        st.success("Analysis completed successfully!")

        st.subheader("OO Metrics Results")

        # Display the combined table
        st.dataframe(
            results,
            use_container_width=True,
            hide_index=True
        )

        # Calculate summary values
        total_classes = len(results)

        total_wmc = sum(
            row["WMC"] for row in results
        )

        avg_com = sum(
            row["COM"] for row in results
        ) / total_classes

        total_cbo = sum(
            row["CBO"] for row in results
        )

        avg_rfc = sum(
            row["RFC"] for row in results
        ) / total_classes

        st.subheader("Metrics Summary")

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Classes", total_classes)
        col2.metric("Total WMC", total_wmc)
        col3.metric("Average COM", f"{avg_com:.2f}")
        col4.metric("Total CBO", total_cbo)
        col5.metric("Average RFC", f"{avg_rfc:.2f}")

        
        # Bar chart for WMC, CBO, and RFC
        st.subheader("Class Metrics Comparison")

        chart_rows = [
            {
                "Class": row["Class"],
                "WMC": row["WMC"],
                "CBO": row["CBO"],
                "RFC": row["RFC"]
            }
            for row in results
        ]

        st.bar_chart(
            chart_rows,
            x="Class",
            y=["WMC", "CBO", "RFC"],
            stack=False
        )


        st.caption(
            "WMC uses unit method weights. "
            "COM uses pairwise shared-attribute cohesion. "
            "CBO counts distinct referenced classes. "
            "RFC counts distinct declared and directly "
            "called attribute-method names."
        )

    except SyntaxError as error:
        st.error(
            f"Python syntax error on line "
            f"{error.lineno}: {error.msg}"
        )

    except ValueError as error:
        st.warning(str(error))
