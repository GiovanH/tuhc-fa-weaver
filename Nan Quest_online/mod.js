module.exports = {
  title: "Nan Quest (online)",
  summary: "MSPFA",

  edit: true,

  trees: {
    './': 'assets://mspfa/Nan Quest_online/',
  },
  async asyncComputed(api) {
    const story = await api.readYamlAsync("./story.yaml")
    return {
      styles: [
        {body: await api.readFileAsync("./adventure.scss")}
      ],
      edit(archive){
        archive.mspfa['Nan Quest_online'] = story
      }
    }
  }
}
