#!/usr/bin/env python3

import json
import openai
import time

model="ada:ft-TODO"

def abstract_to_title(prompt, model="ada:ft-eth-z-rich-2022-09-28-20-17-30", max_tokens=25, n=5):
    prediction = openai.Completion.create(
        model=model,     
        prompt=prompt + " \n\n###\n\n",
        max_tokens=max_tokens,
        stop=[" ###"],
        logprobs=0,
        top_p=1,
        n=n,
    )
  
    titles = [choice["text"].strip() for choice in prediction["choices"]]
#   titles_logprobs = [np.exp(np.sum(choice["logprobs"]["token_logprobs"])) for choice in prediction["choices"]]
#   predicted_reason = prediction["choices"][0]["text"].strip()
  
    return titles, prediction

ABSTRACTS_TITLES = [
    # ("Leveraging machine translation for cross-lingual fine-grained cyberbullying classification amongst pre-adolescents", "Cyberbullying is the wilful and repeated infliction of harm on an individual using the Internet and digital technologies. Similar to face-to-face bullying, cyberbullying can be captured formally using the Routine Activities Model (RAM) whereby the potential victim and bully are brought into proximity of one another via the interaction on online social networking (OSN) platforms. Although the impact of the COVID-19 (SARS-CoV-2) restrictions on the online presence of minors has yet to be fully grasped, studies have reported that 44% of pre-adolescents have encountered more cyberbullying incidents during the COVID-19 lockdown. Transparency reports shared by OSN companies indicate an increased take-downs of cyberbullying-related comments, posts or content by artificially intelligen moderation tools. However, in order to efficiently and effectively detect or identify whether a social media post or comment qualifies as cyberbullying, there are a number factors based on the RAM, which must be taken into account, which includes the identification of cyberbullying roles and forms. This demands the acquisition of large amounts of fine-grained annotated data which is costly and ethically challenging to produce. In addition where fine-grained datasets do exist they may be unavailable in the target language. Manual translation is costly and expensive, however, state-of-the-art neural machine translation offers a workaround. This study presents a first of its kind experiment in leveraging machine translation to automatically translate a unique pre-adolescent cyberbullying gold standard dataset in Italian with fine-grained annotations into English for training and testing a native binary classifier for pre-adolescent cyberbullying. In addition to contributing high-quality English reference translation of the source gold standard, our experiments indicate that the performance of our target binary classifier when trained on machine-translated English output is on par with the source (Italian) classifier.")
    # ("Sequential or jumping: context-adaptive response generation for open-domain dialogue systems", "Neural response generation can automatically produce replies for open-domain dialogue systems without hand-crafted rules or templates. Current studies follow a non-context-adaptive paradigm that employs a single response generator to deal with all dialogues. However, as a dialogue progresses, its textual characteristics (e.g., context length, information volume, involving topics) are changing, so are the issues challenging its response generation. Non-context-adaptive response generators are inflexible and may fail to achieve globally good performance without considering the differences existing among dialogues. In this paper, we propose a novel framework named as C ontext-A daptive R esponse G eneration (CARG), which assembles two different response generators to respectively handle long and short dialogues. Specifically, given a dialogue, CARG first classifies it into short or long types according to the number of its containing utterances. For a short dialogue, CARG employs a sequential reader (SR) to concatenates all utterances into a sequence aiming to construct the dialogue context by limited semantics. For a long dialogue where irrelevant noises and relevant contexts both exist, CARG uses a jumping reader (JR) to generate the response, which treats the latest utterance as the anchor and further performs selective context utilization under its guidance. We introduce ensemble learning strategy to conduct the training and testing of CARG. Extensive experimental results on two benchmark chat corpora show that the proposed CARG framework can outperform various competitive baselines, validating its effectiveness on response generation."),
    # ("Multilingual Transformer Language Model for Speech Recognition in Low-resource Languages", "It is challenging to train and deploy Transformer LMs for hybrid speech recognition 2nd pass re-ranking in low-resource languages due to (1) data scarcity in low-resource languages, (2) expensive computing costs for training and refreshing 100+ monolingual models, and (3) hosting inefficiency considering sparse traffic. In this study, we present a new way to group multiple low-resource locales together and optimize the performance of Multilingual Transformer LMs in ASR. Our Locale-group Multilingual Transformer LMs outperform traditional multilingual LMs along with reducing maintenance costs and operating expenses. Further, for low-resource but high-traffic locales where deploying monolingual models is feasible, we show that fine-tuning our locale-group multilingual LMs produces better monolingual LM candidates than baseline monolingual LMs."),
    # ("Adapting to Non-Centered Languages for Zero-shot Multilingual Translation", "Multilingual neural machine translation can translate unseen language pairs during training, i.e. zero-shot translation. However, the zero-shot translation is always unstable. Although prior works attributed the instability to the domination of central language, e.g. English, we supplement this viewpoint with the strict dependence of non-centered languages. In this work, we propose a simple, lightweight yet effective language-specific modeling method by adapting to non-centered languages and combining the shared information and the language-specific information to counteract the instability of zero-shot translation. Experiments with Transformer on IWSLT17, Europarl, TED talks, and OPUS-100 datasets show that our method not only performs better than strong baselines in centered data conditions but also can easily fit non-centered data conditions. By further investigating the layer attribution, we show that our proposed method can disentangle the coupled representation in the correct direction."),
    ("Towards Sustainable Use of Machine Translation: Usability and Perceived Quality from the End-User Perspective ", "Artificial intelligence-grounded machine translation has fundamentally changed public awareness and attitudes towards multilingual communication. In some language pairs, the accuracy, quality and efficiency of machine-translated texts of certain types can be quite high. Hence, the end-user acceptability and reliance on machine-translated content could be justified. However, machine translation in small and/or low-resource languages might yield significantly lower quality, which in turn may lead to potentially negative consequences and risks if machine translation is used in high-risk contexts without awareness of the drawbacks, critical assessment and modifications to the raw output. The current study, which is part of a more extensive project focusing on the societal impact of machine translation, is aimed at revealing the attitudes towards usability and quality as perceived from the end-user perspective. The research questions addressed revolve around the machine translation types used, purposes of using machine translation, perceived quality of the generated output, and actions taken to improve the quality by users with various backgrounds. The research findings rely on a survey of the population (N = 402) conducted in 2021 in Lithuania. The study reveals the frequent use of machine translation for a diversity of purposes. The most common uses include work, research and studies, and household environments. A higher level of education correlates with user dissatisfaction with the generated quality and actions taken to improve it. The findings also reveal that age correlates with the use of machine translation. Sustainable measures to reduce machine translation related risks have to be established based on the perceptions of different social groups in different societies and cultures."),
    ("DivEMT: Neural Machine Translation Post-Editing Effort Across Typologically Diverse Languages", "We introduce DivEMT, the first publicly available post-editing study of Neural Machine Translation (NMT) over a typologically diverse set of target languages. Using a strictly controlled setup, 18 professional translators were instructed to translate or post-edit the same set of English documents into Arabic, Dutch, Italian, Turkish, Ukrainian, and Vietnamese. During the process, their edits, keystrokes, editing times, pauses, and perceived effort were recorded, enabling an in-depth, cross-lingual evaluation of NMT quality and its post-editing process. Using this new dataset, we assess the impact on translation productivity of two state-of-the-art NMT systems, namely: Google Translate and the open-source multilingual model mBART50. We find that, while post-editing is consistently faster than translation from scratch, the magnitude of its contribution varies largely across systems and languages, ranging from doubled productivity in Dutch and Italian to marginal gains in Arabic, Turkish and Ukrainian, for some of the evaluated modalities. Moreover, the observed cross-language variability appears to partly reflect source-target relatedness and type of target morphology, while remaining hard to predict even based on state-of-the-art automatic MT quality metrics. We publicly release the complete dataset, including all collected behavioural data, to foster new research on the ability of state-of-the-art NMT systems to generate text in typologically diverse languages."),
    ("WeTS: A Benchmark for Translation Suggestion", "Translation Suggestion (TS), which provides alternatives for specific words or phrases given the entire documents translated by machine translation (MT) \cite{lee2021intellicat}, has been proven to play a significant role in post editing (PE). However, there is still no publicly available data set to support in-depth research for this problem, and no reproducible experimental results can be followed by researchers in this community. To break this limitation, we create a benchmark data set for TS, called \emph{WeTS}, which contains golden corpus annotated by expert translators on four translation directions. Apart from the human-annotated golden corpus, we also propose several novel methods to generate synthetic corpus which can substantially improve the performance of TS. With the corpus we construct, we introduce the Transformer-based model for TS, and experimental results show that our model achieves State-Of-The-Art (SOTA) results on all four translation directions, including English-to-German, German-to-English, Chinese-to-English and English-to-Chinese."),
    ("Opportunities for Human-centered Evaluation of Machine Translation Systems", "Machine translation models are embedded in larger user-facing systems. Although model evaluation has matured, evaluation at the systems level is still lacking. We review literature from both the translation studies and HCI communities about who uses machine translation and for what purposes. We emphasize an important difference in evaluating machine translation models versus the physical and cultural systems in which they are embedded. We then propose opportunities for improved measurement of user-facing translation systems. We pay particular attention to the need for design and evaluation to aid engendering trust and enhancing user agency in future machine translation systems."),
    ("Evaluating the Impact of Integrating Similar Translations into Neural Machine Translation", "Previous research has shown that simple methods of augmenting machine translation training data and input sentences with translations of similar sentences (or fuzzy matches), retrieved from a translation memory or bilingual corpus, lead to considerable improvements in translation quality, as assessed by a limited set of automatic evaluation metrics. In this study, we extend this evaluation by calculating a wider range of automated quality metrics that tap into different aspects of translation quality and by performing manual MT error analysis. Moreover, we investigate in more detail how fuzzy matches influence translations and where potential quality improvements could still be made by carrying out a series of quantitative analyses that focus on different characteristics of the retrieved fuzzy matches. The automated evaluation shows that the quality of NFR translations is higher than the NMT baseline in terms of all metrics. However, the manual error analysis did not reveal a difference between the two systems in terms of total number of translation errors; yet, different profiles emerged when considering the types of errors made. Finally, in our analysis of how fuzzy matches influence NFR translations, we identified a number of features that could be used to improve the selection of fuzzy matches for NFR data augmentation."),
    ("A Linguistically Motivated Test Suite to Semi-Automatically Evaluate German–English Machine Translation Output", "This paper presents a fine-grained test suite for the language pair German–English. The test suite is based on a number of linguistically motivated categories and phenomena and the semi-automatic evaluation is carried out with regular expressions. We describe the creation and implementation of the test suite in detail, providing a full list of all categories and phenomena. Furthermore, we present various exemplary applications of our test suite that have been implemented in the past years, like contributions to the Conference of Machine Translation, the usage of the test suite and MT outputs for quality estimation, and the expansion of the test suite to the language pair Portuguese–English. We describe how we tracked the development of the performance of various systems MT systems over the years with the help of the test suite and which categories and phenomena are prone to resulting in MT errors. For the first time, we also make a large part of our test suite publicly available to the research community."),
    # ("Asynchronous haltere input impairs wing and gaze control in Drosophila", "Halteres are multifunctional mechanosensory organs unique to the true flies (Diptera). A set of reduced hindwings, the halteres beat at the same frequency as the lift-generating forewings and sense inertial forces via mechanosensory campaniform sensilla. Though it is well-established that haltere ablation makes stable flight impossible, the specific role of wing-synchronous input has not been established. Using small iron filings attached to the halteres of tethered flies and an alternating electromagnetic field, we experimentally decoupled the wings and halteres of flying Drosophila and observed the resulting changes in wingbeat amplitude and head orientation. We find that providing asynchronous haltere input drives fast saccades in the wing, and that wing and gaze optomotor responses are disrupted differently by asynchronous input. Our findings help to synthesize our understanding of the behavioral deficits that accompany haltere ablation with the known physiology of both haltere neurons and wing and neck muscles."),
    ("Irrigation water depths and soil covers in carrot crop", "The use of soil covers may decrease water consumption and improve the crop sustainability Thus, the objective of this work was to evaluate biophysical parameters and yield of carrot crops (cultivar Brasília) grown under different irrigation water depths and soil cover conditions. The experiment was conducted at the Federal University of Viçosa, MG, Brazil. A randomized block design with four replications was used, in a 5×3 factorial arrangement.The treatments consisted of 5 irrigation water depths, based on the actual soil water capacity (20, 40, 60, 80, and 100% ASWC) and 3 soil covers (white polyethylene, biodegradable semi-kraft paper, and no soil cover - Control). The soil and leaf temperatures, number of leaves, root length, normalized difference vegetation index (NDVI), and fresh root weight were evaluated. The data were subjected to analysis of variance through the F test and the means compared by the Tukey’s test (p≤0.05); regression analysis was carried out using the equation with the highest significant fit. The use of semi-kraft paper was a good option for the carrot crop; and the water depths of up to 60% ASWC did not hinder the crop."),
    ("Activation of innate immunity by neutral polysaccharides from broccoli buds", "Edible substances that stimulate the innate immune system are good candidates for functional foods to improve human health. We have previously reported that acidic polysaccharides from broccoli extract exhibit immunostimulatory effects, but neutral polysaccharides have been overlooked. In the present study, we found that neutral polysaccharides have significantly stronger (higher specific activity) immunostimulatory activity than acidic polysaccharides. The hot water extract of broccoli showed the immunostimulatory activity in the silkworm muscle contraction assay, suggesting that it stimulates innate immunity via paralytic peptide pathway. The activity was concentrated in the buds, but not in the stems and stalk. The active substance was recovered in the flow-through fraction of diethylaminoethyl-cellulose column chromatography with neutral polysaccharides. The specific activity of the fraction was significantly higher than that of the acidic polysaccharides from broccoli reported previously. These results suggest that the neutral polysaccharide present in broccoli buds stimulates innate immunity and can be semi-purified by one-step chromatography."),
    ("Evaluation of Postharvest Senescence in Broccoli Via Hyperspectral Imaging", "Fresh fruits and vegetables are invaluable for human health, but their quality deteriorates before reaching consumers due to ongoing biochemical processes and compositional changes. The current lack of any objective indices for defining “freshness” of fruits or vegetables limits our capacity to control product quality leading to food loss and waste. It has been hypothesized that certain proteins and compounds such as glucosinolates can be used as an indicator to monitor the freshness of vegetables and fruits. However, it is challenging to “visualize” the proteins and bioactive compounds during the senescence processes. In this work, we propose machine learning hyperspectral image analysis approaches for estimating glucosinolates levels to detect postharvest senescence in broccoli. Therefore, we set out the research to quantify glucosinolates as “freshness-indicators” which aid in the development of an innovative and accessible tool to precisely estimate the freshness of produce. Such a tool would allow for significant advancement in postharvest logistics and supporting the availability for high-quality and nutritious fresh produce."),
    ("Broccoli: combining phylogenetic and network analyses for orthology assignment", "Orthology assignment is a key step of comparative genomic studies, for which many bioinformatic tools have been developed. However, all gene clustering pipelines are based on the analysis of protein distances, which are subject to many artefacts. In this paper we introduce Broccoli, a user-friendly pipeline designed to infer, with high precision, orthologous groups and pairs of proteins using a phylogeny-based approach. Briefly, Broccoli performs ultra-fast phylogenetic analyses on most proteins and builds a network of orthologous relationships. Orthologous groups are then identified from the network using a parameter-free machine learning algorithm. Broccoli is also able to detect chimeric proteins resulting from gene-fusion events and to assign these proteins to the corresponding orthologous groups. Tested on two benchmark datasets, Broccoli outperforms current orthology pipelines. In addition, Broccoli is scalable, with runtimes similar to those of recent distance-based pipelines. Given its high level of performance and efficiency, this new pipeline represents a suitable choice for comparative genomic studies.")
]

# small fun out-of-domain stuff
ABSTRACTS_TITLES = [
    ("Review of Liquid-Argon Detectors Development at the CERN Neutrino Platform", "The European Strategy for Particle Physics of 2013 classified the short and long baseline neutrino program as one of the four highest-priority scientific objectives with required international infrastructure. In this framework, CERN has created a \"Neutrino Platform\" for detector R&D and support to future international neutrino experiments, as well as to provide a basis for European neutrino communities towards contributing to the US and Japanese projects. In particular, significant R&D effort is made on the Liquid Argon Time Projection Chamber technologies. As a part of the Neutrino Platform facilities, CERN is constructing a large test area (EHN1 extension of the SPS North Area) with charged beams capabilities devoted to neutrino detectors. An overview will be given of the main Liquid Argon neutrino detector projects presently under development in the framework of the CERN Neutrino platform."),
    ("Particle Physics Aspects of Antihydrogen Studies with ALPHA at CERN", "We discuss aspects of antihydrogen studies, that relate to particle physics ideas and techniques, within the context of the ALPHA experiment at CERN's Antiproton Decelerator facility. We review the fundamental physics motivations for antihydrogen studies, and their potential physics reach. We argue that initial spectroscopy measurements, once antihydrogen is trapped, could provide competitive tests of CPT, possibly probing physics at the Planck Scale. We discuss some of the particle detection techniques used in ALPHA. Preliminary results from commissioning studies of a partial system of the ALPHA Si vertex detector are presented, the results of which highlight the power of annihilation vertex detection capability in antihydrogen studies."),
]

for orig_title, abstract in ABSTRACTS_TITLES:
    titles, results = abstract_to_title(abstract, n=10)
    print(json.dumps({"abstract": abstract, "titles": [orig_title] + titles}))
    input("Press ENTER to continue")