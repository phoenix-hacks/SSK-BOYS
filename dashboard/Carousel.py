from streamlit_carousel import carousel

test_items = [
    dict(
        title="Pradhan Mantri Matru Vandhana Yojna",
        text="This scheme provides a cash incentive of ₹5,000 in three installments to pregnant women",
        img="https://img.freepik.com/free-photo/wide-angle-shot-single-tree-growing-clouded-sky-during-sunset-surrounded-by-grass_181624-22807.jpg?w=1380&t=st=1688825493~exp=1688826093~hmac=cb486d2646b48acbd5a49a32b02bda8330ad7f8a0d53880ce2da471a45ad08a4",
        link="https://wcdhry.gov.in/schemes-for-women/pradhan-mantri-matru-vandhana-yojna/",
    ),
    dict(
        title="Indira Gandhi Maternity Support Scheme (I.G.M.S.Y)",
        text="Launched in 2010, this cash transfer scheme supports pregnant and lactating mothers aged 19+ for their first two live births.",
        img="https://img.freepik.com/free-photo/beautiful-wooden-pathway-going-breathtaking-colorful-trees-forest_181624-5840.jpg?w=1380&t=st=1688825780~exp=1688826380~hmac=dbaa75d8743e501f20f0e820fa77f9e377ec5d558d06635bd3f1f08443bdb2c1",
        link="https://github.com/thomasbs17/streamlit-contributions/tree/master/bootstrap_carousel",
    ),
    dict(
        title="Dr.Muthulakshmi Maternity Benefit Scheme",
        text="This scheme offers financial assistance to poor pregnant mothers",
        img="https://img.freepik.com/free-photo/aerial-beautiful-shot-seashore-with-hills-background-sunset_181624-24143.jpg?w=1380&t=st=1688825798~exp=1688826398~hmac=f623f88d5ece83600dac7e6af29a0230d06619f7305745db387481a4bb5874a0",
        link="https://krishnagiri.nic.in/scheme/dr-muthulakshmi-maternity-benefit-scheme/",
    ),
    dict(
        title="JANANI SURAKSHA YOJANA",
        text="Janani Suraksha Yojana (JSY) is a safe motherhood intervention under the National Health Mission.",
        img="https://img.freepik.com/free-photo/aerial-beautiful-shot-seashore-with-hills-background-sunset_181624-24143.jpg?w=1380&t=st=1688825798~exp=1688826398~hmac=f623f88d5ece83600dac7e6af29a0230d06619f7305745db387481a4bb5874a0",
        link="https://github.com/thomasbs17/streamlit-contributions/tree/master",
    ),
]

carousel(items=test_items)