module.exports = {
  title: "Nan Quest (online)",
  author: "TG Weaver",
  summary: "Nan Quest MSPFA",
  version: 0.1,

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

