module.exports = {
  title: "Ruby Quest (online)",
  summary: "MSPFA",
  
  edit: true,

  trees: {
    './': 'assets://mspfa/Ruby Quest_online/',
  },
  async asyncComputed(api) {
    const story = await api.readYamlAsync("./story.yaml")
    return {
      styles: [
        {body: await api.readFileAsync("./adventure.scss")}
      ],
      edit(archive){
        archive.mspfa['Ruby Quest_online'] = story
      }
    }
  }
}
