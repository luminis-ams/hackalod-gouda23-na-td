<template>
  <h1>Chat with GPT</h1>
  <div style="width: 100%; height: 400px; display: flex">

    <div v-if="loading">
      <h2>Loading!</h2>
    </div>

    <deep-chat
        v-if="!loading"
        ref="chatRef"
        :style="{ width: '100%', height: '100%'}"
        :demo="false"
        :textInput="{ placeholder: { text: 'Welcome to the demo!' } }"
        :initialMessages="initialMessages"
        :request="{url: 'http://localhost:5000/chat'}"
        :stream="false"
        :avatars="true"
        :names="true"
    />


  </div>

</template>

<script setup>
import "deep-chat";
import {ref, onMounted, nextTick} from 'vue';


const messages = ref([])
const chatRef = ref(null)
const loading = ref(true);
const initialMessages = ref([])

// {url: 'http://localhost:5000/openai-chat-stream'}

const initialInformation = {
  "title": [
    "1 ",
    "1"
  ],
  "people": [
    [
      "Vader Johannes Moeder Willemina Oudsen Geboren le Wageningen (Gelderd den 15 December 1883 Laatst gewoond te Badeningen Bij zijne aankomst bij het korp Jang 1.626 Meter. 1. 626 intrede van het 19e levensjaar"
    ],
    [
      "amen der ouders, geboorteplaats, datum van geboorte, laatste woonplaats en signalement. 4"
    ],
    [
      "Vader Moeder Geboren te den Laatst gewoond te Bij zijne aankomst bij het korps lang Meter."
    ],
    [
      "Vader Moeder Geboren te den Laatst gewoond te Bij zijne aankomst bij het korp lang Meter."
    ],
    [
      "Aangezicht ovaal Voorhoofd breed Oogen bruin Neus gewoon Mond klein Kin rond Clona Haar Wenkbrauwen id Merkbare teekenen."
    ],
    [
      "Aangezicht Voorhoofd Oogen Neus Mond Kin Haar Wenkbrauwen Merkbare teekenen"
    ],
    [
      "Aangezicht Voorhoofd Oogen Neus Mond Kin Haar Wenkbrauwen Merkbare teekenen"
    ]
  ],
  "events": [
    [
      "1 December 1902 3 September 1892 14 October 189 Geembarkeerd te Rotterdam a/b 7/m 18„ Semarang weil der löb. 3 September 1898 3 „ 1899 28 December 1894 2 Juli 1900 27 September 190 10 October 190 26 „ 198 29 November 190. 3 Januari 1902 16 Augustus 1902 31 „ 19d=m 25 October 1902 3 „ 1902 2 Juni 1904 24 April 1905 26 „ 1906 Vrijwillig geengageerd als kanonnier voor vier jaren by het leger zoo wel in als buiten Europa in te graant de waarop hij voor den actieren militieren dienst phisiek geschikt bevonden wordt dag van deroekening met ƒ200-premie waarvan  f 20-ne aen den valide comp.s den is en ƒ30- bij overgang naar het Dokoniaal Werfde Gedebarkeerd te Batavia en gepleatst bij het Waper der Artiller Zie Suppletie folio 35104 Gereengageerd voor een jaar bij de Koloniale troepen zoowel in „ 1„ —„ „ —: „ Gedebarkeerd te Batavia en geslaatst als kanonnier 2 klag bij het Wapen der Artillerie als buiten Europa premier ƒ 50 Gereengageerd voor twee jaren bij de Koloniale troepen roowel in als buiten Europa premie of 100 - Overgegaan bij de Veld-Artillerie orporaal K ¬ [DELETE] Ter opzending naar Nederland overgegaan bij het Subskader te Ven nur nicht bekommen, und mit der Wegens tijdelijke lichamelijke ongeschiktheid voor alle militaire diensten, besten om naar Nederland te worden opgezonden derwaarts vertrokken met het W„S Koning Willem I\" te Amsterdam aangekomen en op dato tijde lijk ingedeeld bij de Koloniale Reserve pot, zal worden uitbetaald, terwijl als dan ƒ150- 's Rijkspostspaarbank zal worden ingelegd. Phijsiek geschikt bevonden Korporaal Gedetacheerd naar Oost-Indië en op dato te Amsterdam over gegaan aanboord v/d SS. Prins Hendrik\" Geplaatst by de Veld artellen Kanonnier 2 klasse overgegaan bij de borg istillerie . „ „ vold ontellerie"
    ],
    [
      "Model n°. 178 (binnenvel) Art. 119, § 1. April 1899"
    ],
    [
      "aar — hetzij binnen- of buitenslands — en wanneer in dienst getreden ; omschrijving van het aangegaan akkoord, en de verdere militaire loopbaan. 5"
    ],
    [
      "29 November 1901 25 October 1902 1 December 1902 23 Maart 1903 21 Juli 190 23 September 190 11 November 1904 25 Maart 1904 9 Juli 1907 1. September 1907 3e 26 „ 1907 29 October 1907 Vrijwillig geëngageerd als soldaat voor zes jaren bij het leger zogwel in als buiten Europa met f 300 - premier, wa van ƒ 50 - uitbetaald en f 250 - in ’s Rijkspostspaarbaak en gelegd is. Ingevolge beschikking van het D.I.O.dd 2712 vember 1901. Afd Pers. No 10. Gedetacheerd naar Oost-Indië en op dato te Amsterd 7 overgegaan aan boord van het St. Prins Hendri ick Gedebarkeerd te Batavia en geplaatst bij het 2 Depot - Bat:o vergegaan als Cavalerist 2 klasse bij het Wapen der Cavalerie Fusilie bij het 2e Depot. Bat.o bij het L11- 15 Bat-m Insi Garns Baten. van Palembang R.H. 15 Batn. Insin Bestemd om uiterlijk 2 maande voor het eindige zijner dienst verbintenis voor Nederland te worden opgezonden. Is niet ge neger zich te reenga ageeren; zou des verkiezende tot een zes ja reengagement zijn toegelaten. ter opzending naar Nederland overge- aan Jk Sulx, kader te Batavia dezwaarts vertrokken met het T 35. Koningin Wilhelmina Ostschaept te Amsterdam en op dato terug in de sterfde van het borp"
    ],
    [
      "4 „ 1897 24 „ „ 14 April 190. 28 September „ 19 October „ 1 November „ 29 „ „ 6 Maart 1902 3 November 1902 29 September 1894 5 November „ 6 December „ 1 Mei 1896 30 December „ 22. Juli 1890 1 Augustus „ 8 September „ 20 Mei 1899 2 September 1900 bij evaciatie van Atjel overgegaan bij de Subs: Comp=e van Sum, Westk ter opzending naar Nederland overgegaan bij het Subs: kader te Tadan Wegens tijdelijke lichamelijke ongeschiktheid voor alle mild re diensten bestemd om naar Nederland te worden opgezonden derwaarts vertrokken per SS„ Koning Willem I te Amsterdam aangekomen en op dato tijdelijk ingedeeld bij Koloniale Reserve. Met verbreking van het loopend verband vrijwillig geenga zeerd als Sergeant voor vier jaren bij het leger in Oost of West Indi ingaande met den dag van inscheping met ƒ 200 premie waarvan ƒ20- heden is en f 30 - bij overgang naar het Keloniaal Werfdepot zal worden uitbetaald, terwijl alsdan ƒ150 - in ’s Rijkspostspaarbank zal worden ingelagd Zie Suppletie folio 36489 geembarkeerd te Rotterdam a/b 2/m 18„ Lawoe gedebarkeerd te Batavia in geplaatst bij het 10:e Bat=on In Overgegaan bij het 1e Recruten Bat \"    \"   „   1. Depot „ Korporaal Vergeant afgekeurd voor den dienst te velde bestemd voor Centing dienst Overgegaan bij het Garn: Buten van Palembang voor den dienst te velde weder goed gekeurd ter pasporteezing in Nederland overgegaan bij het Subo, kader te Batar gereengageerd voor 2 jaren bij de koloniale troepen roowel in als buiten Europa premie ƒ 100 - bij het 3 = Bat=m Infie Gedetacheerd naar Oost. Indië en op dato ter uitzending overgegaan naar het Kol, Werdepot"
    ],
    [
      "ijgewoonde veldtochten, bekomen wonden, uitstekende daden wanneer en op welke wijze afgegaan 6"
    ],
    [
      "s t 29 November 1902 Ingeschreven A te Rotterdam a/d/g H„s Ardjoeno „ das wieder selve einge¬ 7 Januari 1903 gedeborkend te Batavia en geplaatst by het 5 Bat. Inf. 12 September 1903 overgegaan by het Subz. ka ader te Semaring 11 Januari 1906 vrywillig onderworpen aan de bepalingen van het pensioen reglement gehecht aan het Kon.besl. van 17 febr. 1905, n 2/8 29 September 1906 geviengageerd voor 4 Jaren om te dienen by de Kol Res: zuwel in als buiten Europa, in te gaan by einde ging der loopen verbinteries, bedongen aan premier ƒ200.- waarvan het 4/4 gedeelte hem by het ingaan van de nieuwe verbentenis zal worden uit betaal zullende als dan het overige te zynen behoeve ingeschreven worde en's Ryse postspaarbank over eenkomstig regelen door den 11. v.K. vast te stellen 29 November 1416 het 1/4 gedeelte der premier ad f 50. - uit betaalic. Scherpschutter 1' maal 29 September 1897 Vernogesteld tot gewoonschutter 12 Maart 1898 „scherpschutter geweer 2' maal den 26' April 1900 16 Augustus 1900 toegekend de Cronzen medaille zonder gratificatie 1900 Krijgsverrichtingen tegen Atjek 19 Februari 1901 Wagenstijselijke kichmanlijke ongeschiktheid voor alle militaire diensten bestemd om naar Naderland te worden opgezonden. Als nog toegekend de gratificatie ad f 12 Eereteeken voor belangenke krijgsbedrijven 1896-1900 - Atjes. 17 april 1907 toegekend de zilveren medaill kruggesteld tot gewoon schutter den 21 Juli 1909 1909 Krijgsvewichtingen in het Gouv- van Clebe„ en Onderh xx"
    ],
    [
      "Richter 2 Klasse Richter 1 Klasse 1' maal 23 Maart 1897 1896-1897 Krijgsverrichtingen tegen Atjek 29 November 1898 toegekend de bronzen medaille zonder gra 1896-1900 Atjes Scherpschutter resolver 1' maal den 9 Juli 190 d Eereteeken voor belangrijke krijgsbedrijven 1873-1896 en Teruggesteld tot richter 2.e kl. den 1.en December 1903 3 Juni 1904. De brouzen medaille ontnomen wegens degrad Richter 1e. kl. 2e. maal 2 December 194 „ § 15 Juni 1906 Vrywillig onderworpen aan de bepalingen van het pensioen reglement gehecht aan het Kon. besl. van 17 Februari 1905, No 8. - 16 Juni 1906 Gereengageerd voor 4 Jaren om te dienen by de Kol. R. zoowel in - als buiten Europa in te gaan by eindiging der loopend verbintenis bedongen aan pr. ƒ 200. waarvan het 1/4 gedeelte he by het ingaren van de nieuwe verbintenis zal worden uit betaald zullende als dan het ovenje te zynen behoeve ingeschreven worden in '/ Ryks postspaarbank aan eenkantig regelen door daar 17.41 vast te stellen 6 Aug.s 1906 het 4 gedeelte des prenue ad f 50.- uitbetaald 29 „ 1906 Kammer Vklasse 1. September 1906 Overgegaar b/d Bergastellerie 3 Juni 1907 Korporaal xx"
    ],
    [
      "1405 Ida id 1 1904 Huijgsverrichtinge tegen Bjerbe 1906 Ida in Midden Sumatras 30 November 1907. Met paspoort wegens diensteindiging Het bewijs van goed gedrag afgegeven"
    ]
  ]
}


onMounted(() => {
  console.log(chatRef)

  fetchInitialMessage()

})

const fetchInitialMessage = async () => {
  const response = await fetch('http://localhost:5000/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      messages: [
        {
          story_page_data: initialInformation
        }
      ]
    })
  });

  const data = await response.json();
  initialMessages.value = [
    {role: "ai", text: data.text},
  ];
  messages.value = [
    {
      role: "ai", text: data.text,
      story_page_data: initialInformation
    },
  ]
  loading.value = false;

  await nextTick(() => {
    hookOnChat()
  })
}

const hookOnChat = () => {
  chatRef.value.requestInterceptor = async (requestDetails) => {
    requestDetails.body.initial_information = initialInformation

    messages.value.push({
      role: "user", text: requestDetails.body.messages[0].text
    });

    requestDetails.body.messages = messages.value

    console.log('Requesting ', requestDetails);
    return requestDetails;
  };

  chatRef.value.responseInterceptor = async (responseDetails) => {
    messages.value.push({
      role: "ai", text: responseDetails.text
    });

    // responseDetails.html = '<b>hello world---------</b>'
    // responseDetails.textz = responseDetails.text
    // responseDetails.text = undefined
    console.log('Response ', responseDetails);
    return responseDetails;
  };


  chatRef.value.onNewMessage = (response) => {
    console.log(response, 'onNewMessage');
  };
}

</script>

<style>
div {
  font-family: sans-serif;
  text-align: center;
  justify-content: center;
  display: grid;
}
</style>
